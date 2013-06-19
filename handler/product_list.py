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
		"""
		Tries to update the ProductList.
		Returns True on success, False otherwise.
		"""
		debug("product_list:update", "fetching data")
		new_values = get_products()
		self.idle.wait()
		if new_values:
			self.data = new_values
			debug("product_list:update", "fetching done")
			return True
		else:
			debug("product_list:update", "fetching failed")
			return False

	def get_name(self, obj_id):
		return self.data[obj_id][0]

	def get_price(self, obj_id):
		return self.data[obj_id][1]

	def contains(self, obj):
		return obj in self.data

PRODUCT_LIST = ProductList()