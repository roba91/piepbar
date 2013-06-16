#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from config import *


def get_products():
	"""
	Queries the products from the intranet and returns a dict containing
	tuples. The dict keys are the ids of the objects (db id). The values
	are tuples of names and prices - {obj_id: (name, price)}, obj_id: int,
	name: String, price: ??.
	"""
	r = requests.get(URL_SYNC, auth=(AUTH_USER, AUTH_PASSWORD))
	data = decode_product_list(r.json())
	print "###################### Products ######################"
	print str(data).replace("),", "),\n")
	print "######################################################"
	return data


def buy(user, *products):
	"""
	Takes a user id (sci login name) and a list of products
	(db id, may still require casting) and adds the bill to the intranet.

	In case of an error, all information must be saved persistently.
	No errors must ever be raised by this function.
	"""
	beverages = encode_buy(products)
	payload = {'buy': {'beverages': beverages, 'user': user}}
	headers = {'content-type': 'application/json'}
	r = requests.post(URL_BUY, data=json.dumps(payload), headers=headers) # TODO: catch ConnectionError and wrong status code

	# TODO: either display error and block until the purchase succeeds, or save