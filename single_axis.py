#!/usr/bin/env python

'''
 ' Single Axis
'''

import os
from farmware_tools import device
from farmware_tools import app
from farmware_tools import get_config_value

x=y=z=0
axis = get_config_value('Single Axis', 'axis', str)
pos = get_config_value('Single Axis', 'pos')
bot_state = device.get_current_position()
log = 'Axis: {}, Position: {}, State: {}'.format(axis, pos, bot_state)
device.log(log, 'info', ['toast'])
