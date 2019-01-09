#!/usr/bin/env python

'''
 ' Single Axis
'''

from farmware_tools import device

import requests
import os

API_TOKEN = os.environ['API_TOKEN']

headers = {'Authorization': 'Bearer ' + API_TOKEN, 'content-type': 'application/json'}
log = {'message': 'Hello Farm!', 'type': 'info'}
response = requests.post('https://my.farmbot.io/api/logs', headers=headers, json=log)
