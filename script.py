#!/usr/bin/env python

'''
 ' Single Axis
'''

import os
from farmware_tools import device
from farmware_tools import app
from farmware_tools import get_config_value
from random import randint

# create Celery coordinate node
coord = device.assemble_coordinate(0, 0, 0)

# get input values
for axis in coords['args']:
	x_lo = 5#int(get_config_value('Random Move Relative', (axis + '_lo')))
 	x_hi = 10#int(get_config_value('Random Move Relative', (axis + '_hi')))
	coord['args'][axis] = randint(x_lo, x_hi)

log = "Random X: {}".format(coord)
device.log(log, 'info', ['toast'])
# perform the move
#device.move_relative(coord, 100, device.assemble_coordinate(0, 0, 0))
