#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
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
	try:
		r = requests.get(URL_SYNC, auth=(AUTH_USER, AUTH_PASSWORD))
		data = decode_product_list(r.json())
		return data
	except Exception:
		return {}


def buy(user, *products):
	"""
	Takes a user id (sci login name) and a list of products
	(db id, may still require casting) and adds the bill to the intranet.

	In case of a communication error this method blocks and retries to
	add the bill to the intranet.

	If the bill was added successfully True is returned. Otherwise,
	if the given user is not allowed to purchase things or a products
	is unknown, False is returned.
	"""
	beverages = encode_buy(products)
	payload = {'buy': {'beverages': beverages, 'user': user}}
	headers = {'content-type': 'application/json'}
	# HTTP-200 -> ok
	# HTTP-422 -> scanned user is not allowed to buy stuff
	# HTTP-otherwise -> something went wrong, retry
	while True:
		try:
			r = requests.post(URL_BUY, data=json.dumps(payload), headers=headers, auth=(AUTH_USER, AUTH_PASSWORD))
			if r.status_code == 200:
				return True
			elif r.status_code == 422:
				return False
			else:
				# something went terribly wrong, retry
				LCD.message_on(**MSG_BUY_RETRY)
				time.sleep(MSG_BUY_RETRY_WAIT)
		except requests.ConnectionError:
			LCD.message_on(**MSG_BUY_RETRY)
			time.sleep(MSG_BUY_RETRY_WAIT)
