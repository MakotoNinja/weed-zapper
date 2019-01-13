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

def delete_all_weeds(points):
	num_weeds = 0
	for point in points:
		if 'weed' in point['name'].lower():
			try:
				app.delete('points', point['id'])
				weeds += 1
			except:
				device.log("App Error - Point ID: {}".format(point['id']))
	return num_weeds

deleted_weeds = del_all_weeds(points)
#device.log('Deleted {} weed points.'.format(deleted_weeds))
device.sync()
