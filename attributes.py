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


def hostnames(vmanage_session):
    response = vmanage_session.get_request("device/monitor")
    items = response.json()['data']

    #login credentials for InfluxDB
    host='localhost'
    port=8086
    USER = 'root'
    PASSWORD = 'root'  
    DBNAME = 'hostnames'

    series = []
    total_records = 0
    json_body = {}
    

    #loop over the API response variable items and create records to be stored in InfluxDB
    for i in items:
        #print(i)
        #print('\n')
        json_body = { "measurement": "devices",
                    "tags": {
                                "host": str(i['host-name']),
                            },
                    #"time": time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(i['entry_time']/1000.)),
                    "fields": {
                                "status": str(i['status'])
                            }
                    }
        #print(json_body)            
        series.append(json_body)
        total_records = total_records+1
    #print(series)

    client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME) 

    print("Create a retention policy")
    retention_policy = 'retention_policy_1'
    client.create_retention_policy(retention_policy, '10d', 3, default=True)


    print("Write points #: {0}".format(total_records))
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
        #print('items')
        #print(i)
        if len(i) == 3:
            json_body = { "measurement": "usernames",
                        "tags": {
                                    "username": str(i['userName']),
                                },
                        #"time": time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(i['entry_time']/1000.)),
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
                        #"time": time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(i['entry_time']/1000.)),
                        "fields": {
                                    "group": str(i['group'])
                                }
                        }
            series.append(json_body)
            total_records = total_records+1

    client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME) 

    print("Create a retention policy")
    retention_policy = 'retention_policy_1'
    client.create_retention_policy(retention_policy, '10d', 3, default=True)


    print("Write points #: {0}".format(total_records))
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
                        "1.1.40.3"
                    ],
                    "field": "vdevice_name",
                    "type": "string",
                    "operator": "in"
                },
                {
                    "value": [
                        "bond_data",
                        "bond_ha",
                        "eth0-1",
                        "eth0-2",
                        "eth1-1",
                        "eth1-2"
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
                    "property": "rx_pkts",
                    "type": "sum"
                },
                {
                    "property": "tx_pkts",
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
                                "tx_pkts": float(i['tx_pkts']),
                                "rx_pkts": float(i['rx_pkts'])
                            }
                    }
        series.append(json_body)
        total_records = total_records+1

    client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)

    print("Create a retention policy")
    retention_policy = 'retention_policy_1'
    client.create_retention_policy(retention_policy, '10d', 3, default=True)

    print("Write points #: {0}".format(total_records))
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
                        "1.1.2.2"
                    ],
                    "field": "vdevice_name",
                    "type": "string",
                    "operator": "in"
                },
                {
                    "value": [
                        "ge0/0",
                        "ge0/1",
                        "system",
                        "ge0/2",
                        "loopback1",
                        "loopback2"
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

    print("Create a retention policy")
    retention_policy = 'retention_policy_1'
    client.create_retention_policy(retention_policy, '10d', 3, default=True)

    print("Write points #: {0}".format(total_records))
    client.write_points(series, retention_policy=retention_policy)

    time.sleep(2)

def CloudExpress(vmanage_session):
    url = "https://sdwandemo.cisco.com:8443/dataservice/device/cloudx/applications"

    querystring = {"deviceId":"1.1.2.22","":"","null":""}

    headers = {
        'User-Agent': "PostmanRuntime/7.22.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "b9249295-5166-4a66-96e1-df1d1c2a376c,de2cbef4-1a68-45d3-ad54-4ef65ec3f3b6",
        'Host': "sdwandemo.cisco.com:8443",
        'Accept-Encoding': "gzip, deflate, br",
        'Cookie': "JSESSIONID=DaxT1ypu31cdQuQfsGoRT-g4qBWNJoIYg1S0N2r4.69c82f90-be13-4083-9bd5-0aec07e6a9e3",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    #response = vmanage_session.get_request("device/cloudx/applications")
    items = response.json()['data']
    

    #login credentials for InfluxDB
    host='localhost'
    port=8086
    USER = 'root'
    PASSWORD = 'root'  
    DBNAME = 'CloudExpress'

    series = []
    total_records = 0
    json_body = {}
    

    #loop over the API response variable items and create records to be stored in InfluxDB
    for i in items:
        print('items')
        print(i)
        '''
        json_body = { "measurement": "usernames",
                    "tags": {
                                "username": str(i['userName']),
                             },
                     #"time": time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(i['entry_time']/1000.)),
                     "fields": {
                                "group": str(i['group'])
                             }
                      }
            series.append(json_body)
            total_records = total_records+1
'''
    client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME) 

    print("Create a retention policy")
    retention_policy = 'retention_policy_1'
    client.create_retention_policy(retention_policy, '10d', 3, default=True)


    print("Write points #: {0}".format(total_records))
    client.write_points(series, retention_policy=retention_policy)

    time.sleep(2)

'''
if __name__ == '__main__':
    # test1.py executed as script
    # do something
'''
    
