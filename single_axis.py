#!/usr/bin/env python

'''
 ' Single Axis
'''

import os
from farmware_tools import device
from farmware_tools import app

x=y=z=0
axis = os.environ.get('axis')
position = os.environ.get('pos')
log = 'Axis: {}, Position:{}'.format(axis, position)
device.log(log, 'info', ['toast'])
