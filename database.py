from __main__ import *
from influxdb import InfluxDBClient

def create_db(databases):
    ###Add databases as a List
    #databases = ['hostnames', 'test1', 'test2', 'test3']

    USER = 'root'
    PASSWORD = 'root'
    host='localhost'
    port=8086

    print('Creating databases')
    client = InfluxDBClient(host, port, USER, PASSWORD)
    for database in databases:
        client.create_database(database)
        client.switch_database(database)

    print('Creating a DB retention policy')
    retention_policy = 'retention_policy_1'
    client.create_retention_policy(retention_policy, '10d', 3, default=True)

if __name__ == '__main__':
    # test1.py executed as script
    # do something
    create_db()
