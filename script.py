#!/usr/bin/env python

'''
 ' Weeding Routine for Farmbot
'''

import os, json
from farmware_tools import device, app, get_config_value
from Coordinate import Coordinate

X_MAX = get_config_value('Weeder Routine', 'x_max')
Y_MAX = get_config_value('Weeder Routine', 'y_max')
Z_MAX = get_config_value('Weeder Routine', 'z_max')

X_MOVE = get_config_value('Weeder Routine', 'x_move')
Y_MOVE = get_config_value('Weeder Routine', 'y_move')
X_START = get_config_value('Weeder Routine', 'x_start')
Y_START = get_config_value('Weeder Routine', 'y_start')

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
	coord = Coordinate(X_START, Y_START)
	offset = device.assemble_coordinate(0, 0, 0)
	device.move_absolute(coord.get(), 100, offset)
	while device.get_current_position('y') < Y_MAX:
		while device.get_current_position('x') < X_MAX:
			# scan for weeds
			device.execute_script(label = 'plant-detection')
			if coord.get_pos('x') + X_MOVE > X_MAX:
				coord.set_pos('x', X_MAX)
			else:
				coord.set_pos('x', coord.get_pos('x') + X_MOVE)
			device.move_absolute(coord.get(), 100, offset)
		if coord.get_pos('y') + Y_MOVE > Y_MAX:
			coord.set_coordinate(X_START, Y_MAX)
		else:
			coord.set_coordinate(X_START, coord.get_pos('y') + Y_MOVE)
		device.move_absolute(coord.get(), 100, offset)
	device.log('Scan Complete.', 'info', ['toast'])

del_all_points(points)
device.sync()
#weed_scan()
#device.sync()

points = app.get_points()
plants = app.get_plants()
device.log("getting tools", 'info')
tools = app.get_toolslots(get_info=app._get_required_info())
device.log("Toos: {}".format(tools), 'info')
#sequence_id = app.find_sequence_by_name(name = )
