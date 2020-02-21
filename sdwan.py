from influxdb import InfluxDBClient
from __main__ import *
import database  #added for DB creation
import attributes
import requests
import sys
import json
import os
import pprint
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning

vmanage_host = os.environ.get("vmanage_host")
vmanage_port = os.environ.get("vmanage_port")
username = os.environ.get("username")
password = os.environ.get("password")

if vmanage_host is None or vmanage_port is None or username is None or password is None:
    print("For Windows Workstation, vManage details must be set via environment variables using below commands")
    print("set vmanage_host=sdwandemo.cisco.com")
    print("set vmanage_port=8443")
    print("set username=demo")
    print("set password=demo")
    print("For MAC OSX Workstation, vManage details must be set via environment variables using below commands")
    print("export vmanage_host=sdwandemo.cisco.com")
    print("export vmanage_port=8443")
    print("export username=demo")
    print("export password=demo")
    exit()

requests.packages.urllib3.disable_warnings()

class rest_api_lib:
    def __init__(self, vmanage_host,vmanage_port, username, password):
        self.vmanage_host = vmanage_host
        self.vmanage_port = vmanage_port
        self.session = {}
        self.login(self.vmanage_host, username, password)

    def login(self, vmanage_host, username, password):

        """Login to vmanage"""

        base_url = 'https://%s:%s/'%(self.vmanage_host, self.vmanage_port)

        login_action = '/j_security_check'

        #Format data for loginForm
        login_data = {'j_username' : username, 'j_password' : password}

        #Url for posting login data
        login_url = base_url + login_action
        url = base_url + login_url

### updated
        #URL for retrieving client token
        token_url = base_url + 'dataservice/client/token'

        sess = requests.session()

        #If the vmanage has a certificate signed by a trusted authority change verify to True

        login_response = sess.post(url=login_url, data=login_data, verify=False)


        if b'<html>' in login_response.content:
            print ("Login Failed")
            sys.exit(0)
        login_token = sess.get(url=token_url, verify=False)

#### updates token
        if login_token.status_code == 200:
            if b'<html>' in login_token.content:
                print ("Login Token Failed")
                exit(0)

        sess.headers['X-XSRF-TOKEN'] = login_token.content
### 
        self.session[vmanage_host] = sess

    def get_request(self, mount_point):
        """GET request"""
        url = "https://%s:%s/dataservice/%s"%(self.vmanage_host, self.vmanage_port, mount_point)
        print(url)

        response = self.session[self.vmanage_host].get(url, verify=False)

        return response

    def post_request(self, mount_point, payload, headers={'Content-type': 'application/json', 'Accept': 'application/json'}):
        """POST request"""
        url = "https://%s:%s/dataservice/%s"%(self.vmanage_host, self.vmanage_port, mount_point)
        #print(url)
        payload = json.dumps(payload)
        #print (payload)

        response = self.session[self.vmanage_host].post(url=url, data=payload, headers=headers, verify=False)
        #print(response.text)
        #exit()
        #data = response
        return response

#add DBs in list form
databases = ['hostnames', 'username', 'interface_bw', 'interface_drops', 'CloudExpress'] 

#Calls database.py, passes DB list, creates DBs in influx on local machine
database.create_db(databases)

#Establishes communication and authenticates to vManage
vmanage_session = rest_api_lib(vmanage_host, vmanage_port, username, password)

#Calls specific functions in Attributes.py 

attributes.hostnames(vmanage_session)

attributes.username(vmanage_session)

attributes.interface_bw(vmanage_session)

attributes.interface_drops(vmanage_session)

attributes.CloudExpress(vmanage_session)


