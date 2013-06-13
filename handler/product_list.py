#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from remote import get_products


class ProductList():
	def __init__(self, *args, **kwargs):
		self.lock = threading.RLock() # mutual exclusion for updates and purchases
		self.update()

	def update(self):
		with self.lock:
			new_values = get_products()
			if new_values:
				self.data = new_values
				print ">>> Updated" # TODO: @display
			else:
				print ">>> Update Failed" # TODO: @display

	def get_name(self, obj_id):
		return self.list[obj_id][0]

	def get_price(self, obj_id):
		return self.list[obj_id][1]

PRODUCT_LIST = ProductList()