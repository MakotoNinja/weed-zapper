#!/usr/bin/env python

'''
 ' Single Axis
'''

from farmware_tools import device
from farmware_tools import app

points = app.get('points')
device.log(points)
