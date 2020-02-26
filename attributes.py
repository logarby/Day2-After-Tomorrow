from __main__ import *
from influxdb import InfluxDBClient
import time
import requests
import json

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


def device(vmanage_session):
    response = vmanage_session.get_request("device/monitor")
    items = response.json()['data']

    #login credentials for InfluxDB
    host='localhost'
    port=8086
    USER = 'root'
    PASSWORD = 'root'
    DBNAME = 'device'

    series = []
    total_records = 0
    json_body = {}


    #loop over the API response variable items and create records to be stored in InfluxDB
    for i in items:
        json_body = { "measurement": "monitor",
              "tags": {
                        "device-model": str(i['device-model']),
                        "device-type": str(i['device-type']),
                        "system-ip": str(i['system-ip']),
                        "host-name": str(i['host-name']),
                        "site-id": int(i['site-id'])
                      },
             "fields": {
                        "status": str(i['status'])
                       }
            }
        series.append(json_body)
        total_records = total_records+1

    client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)

    retention_policy = 'retention_policy_1'
    client.create_retention_policy(retention_policy, '10d', 3, default=True)


    print("Device write points #: {0}".format(total_records))
    client.write_points(series, retention_policy=retention_policy)

    time.sleep(2)

def username(vmanage_session):
    response = vmanage_session.get_request("admin/user")
    items = response.json()['data']


    #login credentials for InfluxDB
    host='localhost'
    port=8086
    USER = 'root'
    PASSWORD = 'root'
    DBNAME = 'username'

    series = []
    total_records = 0
    json_body = {}


    #loop over the API response variable items and create records to be stored in InfluxDB
    for i in items:
        if len(i) == 3:
            json_body = { "measurement": "usernames",
                        "tags": {
                                    "username": str(i['userName']),
                                },
                        "fields": {
                                    "fullname": str(i['description']),
                                    "group": str(i['group'])
                                }
                        }
            series.append(json_body)
            total_records = total_records+1
        else:
            json_body = { "measurement": "usernames",
                        "tags": {
                                    "username": str(i['userName']),
                                },
                        "fields": {
                                    "group": str(i['group'])
                                }
                        }
            series.append(json_body)
            total_records = total_records+1

    client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)

    retention_policy = 'retention_policy_1'
    client.create_retention_policy(retention_policy, '10d', 3, default=True)


    print("Username write points #: {0}".format(total_records))
    client.write_points(series, retention_policy=retention_policy)

    time.sleep(2)

def interface_bw(vmanage_session):

    #login credentials for InfluxDB
    host='localhost'
    port=8086
    USER = 'root'
    PASSWORD = 'root'
    DBNAME = 'interface_bw'

    series = []
    total_records = 0
    json_body = {}

    payload = {
        "query": {
            "condition": "AND",
            "rules": [
                {
                    "value": [
                        "24"
                    ],
                    "field": "entry_time",
                    "type": "date",
                    "operator": "last_n_hours"
                },
                {
                    "value": [
                        "1.1.2.200"
                    ],
                    "field": "vdevice_name",
                    "type": "string",
                    "operator": "in"
                },
                {
                    "value": [
                        "ge0/0",
                        "ge0/1",
                        "ge0/2"
                    ],
                    "field": "interface",
                    "type": "string",
                    "operator": "in"
                }
            ]
        },
        "sort": [
            {
                "field": "entry_time",
                "type": "date",
                "order": "asc"
            }
        ],
        "aggregation": {
            "field": [
                {
                    "property": "interface",
                    "sequence": 1
                }
            ],
            "histogram": {
                "property": "entry_time",
                "type": "minute",
                "interval": 30,
                "order": "asc"
            },
            "metrics": [
                {
                    "property": "rx_kbps",
                    "type": "avg"
                },
                {
                    "property": "tx_kbps",
                    "type": "avg"
                }
            ]
        }
    }

    response = vmanage_session.post_request("statistics/interface/aggregation",payload)

    items = response.json()['data']

    for i in items:
        json_body = { "measurement": "aggregation",
                    "tags": {
                                "interface": str(i['interface'])
                            },
                    "time": time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(i['entry_time']/1000)),
                    "fields": {
                                "tx_kbps": float(i['tx_kbps']),
                                "rx_kbps": float(i['rx_kbps'])
                            }
                    }
        series.append(json_body)
        total_records = total_records+1

    client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)

    retention_policy = 'retention_policy_1'
    client.create_retention_policy(retention_policy, '10d', 3, default=True)

    print("interface BW write points #: {0}".format(total_records))
    client.write_points(series, retention_policy=retention_policy)

    time.sleep(2)

def interface_drops(vmanage_session):

    #login credentials for InfluxDB
    host='localhost'
    port=8086
    USER = 'root'
    PASSWORD = 'root'
    DBNAME = 'interface_drops'

    series = []
    total_records = 0
    json_body = {}

    payload = {
        "query": {
            "condition": "AND",
            "rules": [
                {
                    "value": [
                        "24"
                    ],
                    "field": "entry_time",
                    "type": "date",
                    "operator": "last_n_hours"
                },
                {
                    "value": [
                        "1.1.2.200"
                    ],
                    "field": "vdevice_name",
                    "type": "string",
                    "operator": "in"
                },
                {
                    "value": [
                        "ge0/0",
                        "ge0/1",
                        "ge0/2"
                    ],
                    "field": "interface",
                    "type": "string",
                    "operator": "in"
                }
            ]
        },
        "sort": [
            {
                "field": "entry_time",
                "type": "date",
                "order": "asc"
            }
        ],
        "aggregation": {
            "field": [
                {
                    "property": "interface",
                    "sequence": 1
                }
            ],
            "histogram": {
                "property": "entry_time",
                "type": "minute",
                "interval": 30,
                "order": "asc"
            },
            "metrics": [
                {
                    "property": "rx_drops",
                    "type": "sum"
                },
                {
                    "property": "tx_drops",
                    "type": "sum"
                }
            ]
        }
    }

    response = vmanage_session.post_request("statistics/interface/aggregation",payload)

    items = response.json()['data']

    for i in items:
        json_body = { "measurement": "aggregation",
                    "tags": {
                                "interface": str(i['interface'])
                            },
                    "time": time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(i['entry_time']/1000)),
                    "fields": {
                                "tx_drops": float(i['tx_drops']),
                                "rx_drops": float(i['rx_drops'])
                            }
                    }
        series.append(json_body)
        total_records = total_records+1

    client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)

    retention_policy = 'retention_policy_1'
    client.create_retention_policy(retention_policy, '10d', 3, default=True)

    print("Interface Drops write points #: {0}".format(total_records))
    client.write_points(series, retention_policy=retention_policy)

    time.sleep(2)

def dataCenter1a (vmanage_session):
    response = vmanage_session.get_request("device/interface/synced?deviceId=1.1.2.200")
    items = response.json()['data']

    #login credentials for InfluxDB
    host='localhost'
    port=8086
    USER = 'root'
    PASSWORD = 'root'
    DBNAME = 'dataCenter1a'

    series = []
    total_records = 0
    json_body = {}


    #loop over the API response variable items and create records to be stored in InfluxDB
    for i in items:
        json_body = { "measurement": "device",
              "tags": {
                        "ifname": str(i['ifname']),
                        "ip-address": str(i['ip-address'])
                      },
             "fields": {
                        "if-admin-status": str(i['if-admin-status']),
                        "if-oper-status": str(i['if-oper-status'])
                       }
            }
        series.append(json_body)
        total_records = total_records+1

    client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)

    retention_policy = 'retention_policy_1'
    client.create_retention_policy(retention_policy, '10d', 3, default=True)


    print("DC 1a write points #: {0}".format(total_records))
    client.write_points(series, retention_policy=retention_policy)

    time.sleep(2)
