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
			device.log("App Error - Point ID: {}".format(point['id']), 'error')

def del_all_weeds(points):
	num_weeds = 0
	for point in points:
		if 'weed' in point['name'].lower():
			try:
				app.delete('points', point['id'])
				num_weeds += 1
			except:
				device.log("App Error - Point ID: {}".format(point['id']), 'error')
	return num_weeds

del_all_points(points)
device.sync()
