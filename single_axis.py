#!/usr/bin/env python

'''
 ' Single Axis
'''

from farmware_tools import device
from farmware_tools import app

device.log('Bot is at position {{ x }}, {{ y }}, {{ z }}.', 'success', ['toast'])
