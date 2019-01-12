#!/usr/bin/env python

'''
 ' Random Move Relative
'''

import os
from farmware_tools import device
from farmware_tools import app
from farmware_tools import get_config_value
from random import randint

# coordinate dict
coord = {'x' : 0, 'y' : 0, 'z' : 0}

# loop over axes andd apply a random offset
for axis in coord:
	lo = int(get_config_value('Random Move Relative', (axis + '_lo')))
 	hi = int(get_config_value('Random Move Relative', (axis + '_hi')))
	pos = randint(lo, hi)
	pos *= 1 if randint(0, 1) else -1
	coord[axis] = pos

log = "Moving relative: {}".format(coord)
device.log(log, 'info', ['toast'])
# perform the move
device.move_relative(coord['x'], coord['y'], coord['z'], 100)
