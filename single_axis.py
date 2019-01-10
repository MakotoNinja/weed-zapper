#!/usr/bin/env python

'''
 ' Single Axis
'''

import os
from farmware_tools import device
from farmware_tools import app
from farmware_tools import get_config_value

coord = device.assemble_coordinate(0, 0, 0)
for axis in coord['args']:
	coord['args'][axis] = device.get_current_position(axis)

single_axis = get_config_value('Single Axis', 'axis', str).lower()
coord['args'][single_axis] = int(get_config_value('Single Axis', 'pos'))

log = 'Axis: {}, Coordinate: {}'.format(single_axis, coord)
device.log(log, 'info', ['toast'])
