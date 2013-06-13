#!/usr/bin/env python
# -*- coding: utf-8 -*-


def sync():
	"""
	Fetches all available products and their prices from the
	FS intranet. This function returns a tuple of dicts, ({...}, {...}).

	The first dict contains a price list. The keys are of type int and
	the values are of type ??.

	The second dict contains a name list. The keys are of type int and
	the values are of type string.

	This method always returns a tuple of dicts. If an error occurs,
	empty dicts are returned, i.e. ({},{}).
	"""
	# TODO: fetch the real prices
	return {}, {}


def add_bill(user, *products):
	"""
	Takes a user id (sci login name) and a list of products
	(db id, may still require casting) and adds the bill to the intranet.

	In case of an error, all information must be saved persistently.
	No errors must ever be raised by this function.
	"""
	# TOOD: tell intranet about purchase
	pass