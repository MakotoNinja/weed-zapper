#!/usr/bin/env python

'''
 ' Weeding Routine for Farmbot
'''

import os, sys, json
from random import randint
from farmware_tools import device, app, get_config_value
from Coordinate import Coordinate

input_errors = []
def qualify_int(name):
	data = get_config_value(PKG, name, int)
	try:
		data = int(data)
	except:
		input_errors.append('Must be integer for input: {}.'.format(name))
	else:
		return data

def qualify_sequence(seq_name):
	if len(''.join(seq_name.split())) > 0 and seq_name.lower() != 'none':
		try:
			sequence_id = app.find_sequence_by_name(name = seq_name)
			return sequence_id
		except:
			input_errors.append('Failed to find sequence ID for {}'.format(seq_name))
	return None

def del_all_points():
	for point in points:
		try:
			app.delete('points', point['id'])
		except:
			device.log("App Error - Point ID: {}".format(point['id']), 'error')

def del_all_weeds():
	for point in points:
		if 'weed' in point['name'].lower():
			try:
				app.delete('points', point['id'])
			except:
				device.log("App Error - Point ID: {}".format(point['id']), 'error')
	return num_weeds

def weed_scan():
	""" scans length of X axis """
	def scan_line():
		while device.get_current_position('x') < X_MAX:
			if coord.get_axis_position('x') + X_MOVE > X_MAX:
				coord.set_axis_position('x', X_MAX)
			else:
				coord.set_axis_position('x', coord.get_axis_position('x') + X_MOVE)
			coord.move_abs()
			device.execute_script(label = 'plant-detection')
	""" start scan """
	coord = Coordinate(X_START, Y_START)
	coord.move_abs()
	device.execute_script(label = 'plant-detection')
	scan_line()
	while device.get_current_position('y') < Y_MAX:
		if coord.get_axis_position('y') + Y_MOVE > Y_MAX:
			coord.set_coordinate(X_START, Y_MAX)
		else:
			coord.set_coordinate(X_START, coord.get_axis_position('y') + Y_MOVE)
		coord.move_abs()
		device.execute_script(label = 'plant-detection')
		scan_line()
	device.sync()
	device.log('Scan Complete.', 'info', ['toast'])

def water_weeds():
	device.execute(water_tool_retrieve_sequence_id)
	coord = Coordinate(device.get_current_position('x'), device.get_current_position('y'), Z_TRANSLATE)
	coord.move_abs()
	for weed_point in weed_points:
		coord.set_coordinate(weed_point['x'], weed_point['y'])
		coord.move_abs()
		device.write_pin(PIN_WATER, 1, 0)
		device.wait(1000)
		device.write_pin(PIN_WATER, 0, 0)
	device.execute(water_tool_return_sequence_id)

def smush_weeds():
	coord = Coordinate()
	def move_height():
		coord.set_coordinate(device.get_current_position('x'), device.get_current_position('y'), Z_TRANSLATE)
		coord.move_abs()

	device.execute(weeder_tool_retrieve_sequence_id)
	for weed_point in weed_points:
		move_height()
		coord.set_coordinate(weed_point['x'], weed_point['y'])
		coord.move_abs()
		for i in range(NUM_STABS):
			x = randint(RAN_MIN, RAN_MAX)		# random offset x
			y = randint(RAN_MIN, RAN_MAX)		# random offset y
			x *= 1 if randint(0, 1) else -1		# pos or neg
			y *= 1 if randint(0, 1) else -1		# pos or neg
			coord.set_offset(x, y)				# set the offset
			coord.move_abs()					# move to offset
			coord.set_axis_position('z', Z_MAX)	# set stabbing depth
			coord.move_abs()					# stab weed
			coord.set_axis_position('z', device.get_current_position('z') + Z_RETRACT)	# set retract height
			coord.move_abs()					# retract stabber
	move_height()
	device.execute(weeder_tool_return_sequence_id)

def get_weed_points():
	device.log('Getting weed points of type: {}'.format(WEED_TYPE))
	types = ['weed', 'safe-remove weed'] if WEED_TYPE == 'both' else [WEED_TYPE]
	device.log('Weed Type(s): {}'.format(json.dumps(types)))
	wp = []
	for point in points:
		if point['name'].lower() in types:
			wp.append(point)
	return wp

PIN_LIGHTS = 7
PIN_WATER = 8
PKG = 'Weeder Routine'
X_START = qualify_int('x_start')
Y_START = qualify_int('y_start')
X_MAX = qualify_int('x_max')
Y_MAX = qualify_int('y_max')
Z_MAX = qualify_int('z_max')
Z_TRANSLATE = qualify_int('z_translate')
X_MOVE = qualify_int('x_move')
Y_MOVE = qualify_int('y_move')
NUM_STABS = qualify_int('num_stabs')
RAN_MIN = qualify_int('ran_min')
RAN_MAX = qualify_int('ran_max')
Z_RETRACT = qualify_int('z_retract')

WEED_TYPE = get_config_value(PKG, 'weed_type', str).lower()
if WEED_TYPE not in ['weed', 'safe-remove', 'both']:
	device.log('Weed type invalid. Must be WEED, SAFE-REMOVE or BOTH', 'error')
	sys.exit()

water_tool_retrieve_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_water_retrieve', str)) #optional
water_tool_return_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_water_return', str)) #optional
weeder_tool_retrieve_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_weed_retrieve', str))
weeder_tool_return_sequence_id = qualify_sequence(get_config_value(PKG, 'tool_weed_return', str))

if len(input_errors):
	for err in input_errors:
		device.log(err, 'error', ['toast'])
	sys.exit()
else:
	device.log('No config errors detected')

device.write_pin(PIN_LIGHTS, 1, 0)

points = app.get_points()
if len(points):
	device.log('Deleting existing points...')
	del_all_points()
	device.sync()

weed_scan()
points = app.get_points()
weed_points = get_weed_points()
if len(weed_points):
	if water_tool_retrieve_sequence_id:
		water_weeds()
	smush_weeds()
else:
	device.log('No weeds detected, going home...')
device.home('all')
device.write_pin(PIN_LIGHTS, 0, 0)
