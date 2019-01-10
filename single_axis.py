#!/usr/bin/env python

'''
 ' Single Axis
'''

import os
from farmware_tools import device
from farmware_tools import app
from farmware_tools import get_config_value

# create Celery coordinate node
coord = device.assemble_coordinate(0, 0, 0)
# apply currrent positions to coordinate node
for axis in coord['args']:
	coord['args'][axis] = device.get_current_position(axis)
# get the desired axis to modify and set the coordinate node to the desired value
single_axis = get_config_value('Single Axis', 'axis', str).lower()
coord['args'][single_axis] = int(get_config_value('Single Axis', 'pos'))

#log = 'Axis: {}, Coordinate: {}'.format(single_axis, coord)
log = "Moving '%s' axis to %d" % (single_axis, coord['args'][single_axis])
device.log(log, 'info', ['toast'])
# perform the move
device.move_absolute(coord)
