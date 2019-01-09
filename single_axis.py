#!/usr/bin/env python

'''
 ' Single Axis
'''

from farmware_tools import device

import requests
import os

API_TOKEN = os.environ['API_TOKEN']
FARMWARE_URL = os.environ['FARMWARE_URL']

headers = {'Authorization': 'Bearer ' + API_TOKEN, 'content-type': 'application/json'}
log = {'message': 'Hello Farm!', 'type': 'info'}
response = requests.post(FARMWARE_URL, headers=headers, json=log)
