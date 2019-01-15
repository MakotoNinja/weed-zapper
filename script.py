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
	if len(''.join(seq_name.split())) > 0 and seq_name.lower() != 'none':
		try:
			sequence_id = app.find_sequence_by_name(name = seq_name)
			return sequence_id
		except:
			input_errors.append('Failed to find sequence ID for {}'.format(seq_name))
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
	device.sync()
	device.log('Scan Complete.', 'info', ['toast'])

def water_weeds():
	global PIN_WATER
	global points, get_water_tool_sequence_id
	device.execute(get_water_tool_sequence_id)
	coord = Coordinate(0, 0)
	offset = device.assemble_coordinate(0,0,0)
	for point in points:
		if 'weed' in point['name'].lower():
			coord.set_coordinate(point['x'], point['y'])
			device.move_absolute(coord, 100, offset)
			device.write_pin(PIN_WATER, 1, 0)
			wait(2000)
			device.write_pin(PIN_WATER, 0, 0)

PIN_WATER = 8
PKG = 'Weeder Routine'
X_START = qualify_int(PKG, 'x_start')
Y_START = qualify_int(PKG, 'y_start')
X_MAX = qualify_int(PKG, 'x_max')
Y_MAX = qualify_int(PKG, 'y_max')
Z_MAX = qualify_int(PKG, 'z_max')
X_MOVE = qualify_int(PKG, 'x_move')
Y_MOVE = qualify_int(PKG, 'y_move')

get_water_tool_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_water', str)) #optional
get_weeder_tool_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_weed', str))

if len(input_errors):
	for err in input_errors:
		device.log(err, 'error', ['toast'])
	sys.exit()

points = app.get_points()
del_all_points(points)
device.sync()
weed_scan()

points = app.get_points()
if len(points):
	if get_water_tool_sequence_id:
		water_weeds()
	else:
		device.execute(get_weeder_tool_sequence_id)

"""
del_all_points(points)
device.sync()
weed_scan()
device.sync()
"""
