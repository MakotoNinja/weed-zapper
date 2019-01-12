#!/usr/bin/env python

'''
 ' Playing with points
'''

import os
from farmware_tools import device, app
from farmware_tools import get_config_value

points = app.get_points()
plants = app.get_plants()

log = "Points: {}".format(json.dumps(points))
device.log(log, 'info', ['toast'])

log = "Plants: {}".format(json.dumps(plants))
device.log(log, 'info', ['toast'])
