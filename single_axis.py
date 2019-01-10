#!/usr/bin/env python

'''
 ' Single Axis
'''

from farmware_tools import device

device.log('Hello Farm.', 'info', ['toast'])
device.move_relative(x=0, y=100, z=0, speed=100)
device.log('Bot is at position {{ x }}, {{ y }}, {{ z }}.')
