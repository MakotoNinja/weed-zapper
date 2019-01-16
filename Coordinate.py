#!/usr/bin/env python

from farmware_tools import device, app

class Coordinate:
	def __init__(self, x=0, y=0, z=0, ox=0, oy=0, oz=0):
		self.coordinate = device.assemble_coordinate(x, y, z)
		self.offset = device.assemble_coordinate(ox, oy, oz)

	def set_pos(self, axis, pos):
		self.coordinate['args'][axis] = pos

	def get_pos(self, axis):
		return self.coordinate['args'][axis]

	def get_coordinate(self):
		return self.coordinate['args']

	def set_coordinate(self, x=0, y=0, z=0):
		self.coordinate['args']['x'] = x
		self.coordinate['args']['y'] = y
		self.coordinate['args']['z'] = z

	def get(self):
		return self.coordinate

	def set_offset_pos(self, axis, pos):
		self.offset['args'][axis] = pos

	def get_offset_pos(self, axis):
		return self.offset['args'][axis]

	def get_offset(self):
		return self.offset

	def set_offset(self, x, y, z):
		self.offset['args']['x'] = x
		self.offset['args']['y'] = y
		self.offset['args']['z'] = z

	def print_me(self):
		print(self.get_coordinate())

	def print_offset(self):
		print(self.get_offset())
