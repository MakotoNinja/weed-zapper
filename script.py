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
coord = {
	'x' : 0,
	'y' : 0,
	'z' : 0
}

# get input values
for axis in coord:
	lo = int(get_config_value('Random Move Relative', (axis + '_lo')))
 	hi = int(get_config_value('Random Move Relative', (axis + '_hi')))
	pos = randint(lo, hi)
	if not randint(0, 1): pos *= -1
	coord[axis] = pos

log = "Moving relative: {}".format(coord)
device.log(log, 'info', ['toast'])
# perform the move
device.move_relative(coord['x'], coord['x'], coord['z'], 100)
