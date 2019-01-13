#!/usr/bin/env python

'''
 ' Weeding Routine for Farmbot
'''

import os, json
from farmware_tools import device, app, get_config_value

X_MAX = get_config_value('Weeder Routine', 'x_max')
Y_MAX = get_config_value('Weeder Routine', 'y_max')
Z_MAX = get_config_value('Weeder Routine', 'z_max')

X_MOVE = get_config_value('Weeder Routine', 'x_move')
Y_MOVE = get_config_value('Weeder Routine', 'y_move')

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

def mod_coord(coord, x, y, z):
	coord['args']['x'] = x
	coord['args']['y'] = y
	coord['args']['z'] = z
	return coord

def get_pos(coord, axis):
	return coord['args'][axis]

def set_pos(coord, axis, value):
	return coord['args'][axis]

def weed_scan():
	coord = device.assemble_coordinate(50, 50, 0)
	offset = device.assemble_coordinate(0, 0, 0)
	device.move_absolute(coord, 100, offset)
	while get_pos(coord, 'y') < Y_MAX - Y_MOVE:
		while get_pos(coord, 'x') < X_MAX - X_MOVE:
			#device.execute_script(label = 'plant-detecttion')
			coord = set_pos(coord, 'x', get_pos(coord, 'x') + X_MOVE)
			device.move_absolute(coord, 100, offset)
		coord = set_pos(coord, 'y', get_pos(coord, 'y') + Y_MOVE)
		device.move_absolute(coord, 100, offset)
	device.log('Scan Complete.', 'info', ['toast'])
#del_all_points(points)
#device.sync()

#device.execute_script(label='my-farmware')
del_all_points(points)
weed_scan()
