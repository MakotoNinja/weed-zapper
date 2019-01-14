#!/usr/bin/env python

'''
 ' Weeding Routine for Farmbot
'''

import os, sys, json
from farmware_tools import device, app, get_config_value
from Coordinate import Coordinate

input_errors = []
def qualify_input(package, name, data_type):
	global input_errors
	data = get_config_value(package, name, data_type)
	if data_type == int:
		try:
			data = int(data)
		except:
			input_errors.append('Must be integer for input: {}.'.format(name))
		else:
			return data
	elif data_type == str:
		if len(''.join(data.split())) <= 0:
			input_errors.append('Nothing was entered for input: {}.'.format(name))
		else:
			return data
	return None


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

X_START = qualify_input('Weeder Routine', 'x_start', int)
Y_START = qualify_input('Weeder Routine', 'y_start', int)
X_MAX = qualify_input('Weeder Routine', 'x_max', int)
Y_MAX = qualify_input('Weeder Routine', 'y_max', int)
Z_MAX = qualify_input('Weeder Routine', 'z_max', int)
X_MOVE = qualify_input('Weeder Routine', 'x_move', int)
Y_MOVE = qualify_input('Weeder Routine', 'y_move', int)

tool_water = get_config_value('Weeder Routine', 'tool_water', str) #optional
tool_weed = qualify_input('Weeder Routine', 'tool_weed', str)

points = app.get_points()
plants = app.get_plants()

if len(input_errors):
	for err in input_errors:
		device.log(err, 'error', ['toast'])
	sys.exit()

device.log('Tool Water: {}, Type: {}'.format(tool_water, type(tool_water)), 'info', ['toast'])
try:
	sequence_id = app.find_sequence_by_name(name = tool_water)
except:
	device.log('Failed to find sequence ID for {}'.format(tool_water), 'info', ['toast'])

"""
del_all_points(points)
device.sync()
weed_scan()
device.sync()
"""
points = app.get_points()
plants = app.get_plants()
