#!/usr/bin/env python

'''
 ' Weeding Routine for Farmbot
'''

import os, json
from farmware_tools import device, app, get_config_value
from Coordinate import Coordinate
"""
X_MAX = get_config_value('Weeder Routine', 'x_max')
Y_MAX = get_config_value('Weeder Routine', 'y_max')
Z_MAX = get_config_value('Weeder Routine', 'z_max')

X_MOVE = get_config_value('Weeder Routine', 'x_move')
Y_MOVE = get_config_value('Weeder Routine', 'y_move')
"""
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

def weed_scan():
	coord = Coordinate(50,50)
	offset = device.assemble_coordinate(0, 0, 0)
	device.move_absolute(coord.get(), 100, offset)
	while device.get_current_position('y') < Y_MAX - Y_MOVE:
		while device.get_current_position('x') < X_MAX - X_MOVE:
			coord.set_pos('x', coord.get_pos('x') + X_MOVE)
			device.move_absolute(coord.get(), 100, offset)
		coord.set_coordinate(50, coord.get_pos('y') + Y_MOVE)
		device.move_absolute(coord.get(), 100, offset)
	device.log('Scan Complete.', 'info', ['toast'])

#del_all_points(points)
#device.sync()

#device.execute_script(label='my-farmware')
del_all_points(points)
weed_scan()
