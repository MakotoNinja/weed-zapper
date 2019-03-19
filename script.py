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
		device.wait(3000)
		device.execute_script(label = 'plant-detection')
	""" scans length of X axis """
	def scan_line():
		while device.get_current_position('x') < X_MAX:
			if coord.get_axis_position('x') + X_MOVE > X_MAX:
				coord.set_axis_position('x', X_MAX)
			else:
				coord.set_axis_position('x', coord.get_axis_position('x') + X_MOVE)
			coord.move_abs()
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
	coord = Coordinate()
	device.execute(weeder_tool_retrieve_sequence_id)
	for weed_point in weed_points:
		coord.set_coordinate(device.get_current_position('x'), device.get_current_position('y'), Z_TRANSLATE)
		coord.set_coordinate(weed_point['x'] - (AREA_SIZE / 2), weed_point['y'] - (AREA_SIZE / 2))
		coord.set_axis_position('z', ZAP_HEIGHT)
		device.write_pin(PIN_ZAPPER, 1, 0)
		i = j = 0
		while(i < AREA_SIZE):
			if coord.get_offset_axis_position('x') > 0:
				coord.set_offset_axis_position('x', coord.get_axis_position('x') + AREA_SIZE)
				increment = -1
			else:
				coord.set_offset_axis_position('x', 0, False)
				increment = 1
			while(j < AREA_SIZE):
				coord.set_offset_axis_position('x', coord.get_offset_axis_position('x') + increment)
				j += 1
			j = 0
			coord.set_offset_axis_position('y', coord.get_offset_axis_position('y') + 1)
			i += 1
		device.write_pin(PIN_ZAPPER, 0, 0)
	coord.set_coordinate(device.get_current_position('x'), device.get_current_position('y'), Z_TRANSLATE)
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
device.log('INIT')
X_START = Qualify.integer(PKG, 'x_start')
device.log('X_START: {}'.format(X_START))
Y_START = Qualify.int(PKG, 'y_start')
X_MAX = Qualify.integer(PKG, 'x_max')
Y_MAX = Qualify.integer(PKG, 'y_max')
ZAP_HEIGHT = Qualify.integer(PKG, 'zap_height')
Z_TRANSLATE = Qualify.integer('z_translate')
X_MOVE = Qualify.integer(PKG, 'x_move')
Y_MOVE = Qualify.integer(PKG, 'y_move')
AREA_SIZE = Qualify.integer(PKG, 'area_size')
device.log('AREA_SIZE: {}'.format(AREA_SIZE))
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
if len(weed_points):
	if water_tool_retrieve_sequence_id:
		water_weeds()
	zap_weeds()
else:
	device.log('No weeds detected, going home...')
device.home('all')
device.write_pin(PIN_LIGHTS, 0, 0)
