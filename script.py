#!/usr/bin/env python

'''
 ' Playing with points
'''

import os
from farmware_tools import device, app
from farmware_tools import get_config_value

points = app.get_points()

log = "Points: {}".format(points)
device.log(log, 'info', ['toast'])
