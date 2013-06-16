#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from remote import get_products


class ProductList():
	def __init__(self, *args, **kwargs):
		self.idle = threading.Event()
		self.idle.set()
		self.data = {} # {data: (name, price)}
		self.update()

	def update(self):
		new_values = get_products()
		self.idle.wait()
		if new_values:
			self.data = new_values
			print ">>> Updated" # TODO: @display
		else:
			print ">>> Update Failed" # TODO: @display

	def get_name(self, obj_id):
		return self.data[obj_id][0]

	def get_price(self, obj_id):
		return self.data[obj_id][1]

	def contains(self, obj):
		return obj in self.data

PRODUCT_LIST = ProductList()