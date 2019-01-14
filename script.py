#!/usr/bin/env python

'''
 ' Weeding Routine for Farmbot
'''

import os, sys, json
from farmware_tools import device, app, get_config_value
from Coordinate import Coordinate

input_errors = []
def qualify_int(package, name):
	global input_errors
	data = get_config_value(package, name, int)
	try:
		data = int(data)
	except:
		input_errors.append('Must be integer for input: {}.'.format(name))
	else:
		return data

def qualify_sequence(seq_name):
	global input_errors
	if len(''.join(seq_name.split())) > 0 and not seq_name.lower() == 'none':
		try:
			sequence_id = app.find_sequence_by_name(name = seq_name)
		except:
			input_errors.append('Failed to find sequence ID for {}'.format(seq_name))
		return sequence_id
	elif len(''.join(seq_name.split())) <= 0:
		input_errors.append('Enter "None" if no sequence is desired for {}'.format(seq_name))

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

PACKAGE = 'Weeder Routine'
X_START = qualify_int(PACKAGE, 'x_start')
Y_START = qualify_int(PACKAGE, 'y_start')
X_MAX = qualify_int(PACKAGE, 'x_max')
Y_MAX = qualify_int(PACKAGE, 'y_max')
Z_MAX = qualify_int(PACKAGE, 'z_max')
X_MOVE = qualify_int(PACKAGE, 'x_move')
Y_MOVE = qualify_int(PACKAGE, 'y_move')

#tool_water = qualify_sequence(PACKAGE, 'tool_water', str) #optional
#tool_weed = qualify_sequence(PACKAGE, 'tool_weed', str)

points = app.get_points()
plants = app.get_plants()

if len(input_errors):
	for err in input_errors:
		device.log(err, 'error', ['toast'])
	sys.exit()
"""
del_all_points(points)
device.sync()
weed_scan()
device.sync()
"""
points = app.get_points()
plants = app.get_plants()
