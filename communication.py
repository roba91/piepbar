#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_remote_prices():
	"""
	Return as a dict with item and price information (item x price).
	This method always returns an dict. If some error occurs an
	empty dict ({}) is returned.
	"""
	# TODO: fetch the real prices
	return {}

def add_bill(user, *products):
	"""
	Takes a user id (sci login name) and a list of products
	(db id, may still require casting) and adds the bill to the intranet.

	In case of an error, all information must be saved persistently.
	No errors must ever be raised by this function.
	"""
	# TOOD: tell intranet about purchase
	pass