#!/usr/bin/env python

'''
 ' Single Axis
'''

from farmware_tools import device

device.log('Bot is at position {{ x }}, {{ y }}, {{ z }}.', 'success', ['toast'])
