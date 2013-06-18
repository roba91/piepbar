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

	In case of an error, all information must be saved persistently.
	No errors must ever be raised by this function.
	"""
	beverages = encode_buy(products)
	payload = {'buy': {'beverages': beverages, 'user': user}}
	headers = {'content-type': 'application/json'}
	def perform_purchase(url, data, head):
		try:
			r = requests.post(url, data=data, headers=head, auth=(AUTH_USER, AUTH_PASSWORD))
			return r.status_code == 200
		except requests.ConnectionError:
			return False
	error = False
	while not perform_purchase(URL_BUY, json.dumps(payload), headers):
		if not error:
			# do not permanently refresh the display with the same thing
			LCD.message_on(**MSG_BUY_RETRY)
			error = True
		time.sleep(MSG_BUY_RETRY_WAIT)
