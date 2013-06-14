#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_products():
	"""
	Queries the products from the intranet and returns a dict containing
	tuples. The dict keys are the ids of the objects (db id). The values
	are tuples of names and prices - {obj_id: (name, price)}, obj_id: int,
	name: String, price: ??.
	"""
	# TODO: fetch the real prices
	return {}


def buy(user, *products):
	"""
	Takes a user id (sci login name) and a list of products
	(db id, may still require casting) and adds the bill to the intranet.

	In case of an error, all information must be saved persistently.
	No errors must ever be raised by this function.
	"""
	# TOOD: tell intranet about purchase
	pass