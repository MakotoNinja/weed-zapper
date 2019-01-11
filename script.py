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

rand_vals = {
	'x' : {'lo' : 0, 'hi' : 0},
	'y' : {'lo' : 0, 'hi' : 0},
	'z' : {'lo' : 0, 'hi' : 0},
}
# get input values
for axis in rand_vals:
	rand_vals[axis]['lo'] = int(get_config_value('Random Move Relative', axis + '_lo'))
 	rand_vals[axis]['hi'] = int(get_config_value('Random Move Relative', axis + '_hi'))


#log = 'Axis: {}, Coordinate: {}'.format(single_axis, coord)
log = "Random X: {}".format(rand_vals)
device.log(log, 'info', ['toast'])
# perform the move
#device.move_absolute(coord, 100, device.assemble_coordinate(0, 0, 0))
