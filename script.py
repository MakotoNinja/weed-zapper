#!/usr/bin/env python

'''
 ' Playing with points
'''

import os, json
from farmware_tools import device, app
from farmware_tools import get_config_value

points = app.get_points()
plants = app.get_plants()

def del_all_points():
	for point in points:
		app.delete(point['id'])

del_all_points()
device.sync()
