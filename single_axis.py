#!/usr/bin/env python

'''
 ' Single Axis
'''

import os
from farmware_tools import device
from farmware_tools import app
from farmware_tools import get_config_value

coord = device.assemble_coordinate(0, 0, 0)
#for position in positions:
#	positions[position] = device.get_current_position(position)

axis = get_config_value('Single Axis', 'axis', str).lower()
#positions[axis] = int(get_config_value('Single Axis', 'pos'))

log = 'Axis: {}, Coordinate: {}'.format(axis, coord)
device.log(log, 'info', ['toast'])
