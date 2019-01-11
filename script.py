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
x_lo = int(get_config_value('Random Move Relative', 'x_lo'))
x_hi = int(get_config_value('Random Move Relative', 'x_hi'))
x_ran = randint(x_lo, x_hi)

#log = 'Axis: {}, Coordinate: {}'.format(single_axis, coord)
log = "Random X: {}".format(x_ran)
device.log(log, 'info', ['toast'])
# perform the move
#device.move_absolute(coord, 100, device.assemble_coordinate(0, 0, 0))
