#!/usr/bin/env python

'''
 ' Single Axis
'''

import os
from farmware_tools import device
from farmware_tools import app
from farmware_tools import get_config_value

positions = {'x' : 0, 'y' : 0, 'z' : 0}
for position in positions:
	positions[position] = device.get_current_position(position)

axis = get_config_value('Single Axis', 'axis', str).lower()
positions[axis] = get_config_value('Single Axis', 'pos')

log = 'Axis: {}, Position: {}, State: {}'.format(axis, pos, positions)
device.log(log, 'info', ['toast'])
