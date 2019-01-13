#!/usr/bin/env python

'''
 ' Playing with points
'''

import os, json
from farmware_tools import device, app, get_config_value

points = app.get_points()
plants = app.get_plants()

def del_all_points(points):
	for point in points:
		try:
			app.delete('points', point['id'])
		except:
			device.log("App Error - Point ID: {}".format(point['id']))

del_all_points(points)
device.sync()
