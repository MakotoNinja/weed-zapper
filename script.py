#!/usr/bin/env python

'''
 ' Weeding Routine for Farmbot
'''

import os, sys, json, Qualify
from random import randint
from farmware_tools import device, app, get_config_value
from Coordinate import Coordinate

input_errors = []
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
	""" pause before taking image """
	def plant_detection():
		device.wait(1000)
		device.execute_script(label = 'plant-detection')
	""" scans length of X axis """
	def scan_line():
		while device.get_current_position('x') < X_MAX:
			if coord.get_axis_position('x') + X_MOVE > X_MAX:
				coord.set_axis_position('x', X_MAX)
			else:
				coord.set_axis_position('x', coord.get_axis_position('x') + X_MOVE)
			plant_detection();
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
		plant_detection();
		scan_line()
	device.sync()
	device.log('Scan Complete.', 'info', ['toast'])

def zap_weeds():
	device.execute(weeder_tool_retrieve_sequence_id)
	coord = Coordinate(device.get_current_position('x') + LASER_OFFSET_X, device.get_current_position('y') + LASER_OFFSET_Y)
	device.log('coord: {}'.format(json.dumps(coord.get_coordinate())))
	for weed_point in weed_points:
		coord.set_coordinate(z=Z_TRANSLATE)						# move up to translate height
		coord.set_coordinate(weed_point['x'], weed_point['y'])	# move to point
		coord.set_axis_position('z', ZAP_HEIGHT)				# move down to zapping height
		coord.set_offset(-(AREA_SIZE / 2), -(AREA_SIZE / 2))	# offset x and y half of area
		coord.set_speed(1)
		device.write_pin(PIN_ZAPPER, 1, 0)
		for i in range(AREA_SIZE):
			if coord.get_offset_axis_position('x') > 0:
				coord.set_offset_axis_position('x', -(AREA_SIZE / 2))
			else:
				coord.set_offset_axis_position('x', AREA_SIZE / 2)
			coord.set_offset_axis_position('y', coord.get_offset_axis_position('y') + 1)
		device.write_pin(PIN_ZAPPER, 0, 0)
		coord.set_speed(100)
		coord.set_coordinate(z=Z_TRANSLATE)
	device.execute(weeder_tool_return_sequence_id)

def get_weed_points():
	device.log('Getting weed points of type: "{}""'.format(WEED_TYPE))
	types = ['weed', 'safe-remove weed'] if WEED_TYPE == 'both' else [WEED_TYPE]
	device.log('Weed Type(s): {}'.format(json.dumps(types)))
	wp = []
	for point in points:
		if point['name'].lower() in types:
			wp.append(point)
	return wp

PIN_LIGHTS = 7
PIN_WATER = 8
PIN_ZAPPER = 10
PKG = 'Weed Zapper'

X_START = Qualify.integer(PKG, 'x_start')
Y_START = Qualify.integer(PKG, 'y_start')
X_MAX = Qualify.integer(PKG, 'x_max')
Y_MAX = Qualify.integer(PKG, 'y_max')
ZAP_HEIGHT = Qualify.integer(PKG, 'zap_height')
Z_TRANSLATE = Qualify.integer(PKG, 'z_translate')
X_MOVE = Qualify.integer(PKG, 'x_move')
Y_MOVE = Qualify.integer(PKG, 'y_move')
AREA_SIZE = Qualify.integer(PKG, 'area_size')
LASER_OFFSET_X = Qualify.integer(PKG, 'offset_x')
LASER_OFFSET_Y = Qualify.integer(PKG, 'offset_y')

WEED_TYPE = get_config_value(PKG, 'weed_type', str).lower()
if WEED_TYPE not in ['weed', 'safe-remove', 'both']:
	device.log('Weed type invalid. Must be WEED, SAFE-REMOVE or BOTH', 'error')
	sys.exit()

weeder_tool_retrieve_sequence_id = Qualify.sequence(PKG, 'tool_weed_retrieve')
weeder_tool_return_sequence_id = Qualify.sequence(PKG, 'tool_weed_return')

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
#device.log(json.dumps(weed_points))
if len(weed_points):
	zap_weeds()
else:
	device.log('No weeds detected, going home...')
device.home('all')
device.write_pin(PIN_LIGHTS, 0, 0)
