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
		# print str(data).replace("),", "),\n")
		debug("remote:get_products", "successfully read data")
		return data
	except Exception, e:
		debug("remote:get_products", "fetching failed; %s: %s" % (type(e).__name__, e))
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
	debug("remote:buy", "init buy sequence")
	try_sync = True
	while True:
		try:
			r = requests.post(URL_BUY, data=json.dumps(payload), headers=headers, auth=(AUTH_USER, AUTH_PASSWORD))
			if r.status_code == 200:
				debug("remote:buy", "...everything worked fine")
				return True
			elif r.status_code == 422:
				# sync
				if not try_sync:
					debug("remote:buy", "...did not work (user or product unknown by FSIntra)")
					return False
				else:
					debug("remote:buy", "...did not work (user or product unknown by FSIntra) -> syncing")
					try_sync = True
					from product_list import PRODUCT_LIST
					PRODUCT_LIST.update()
			else:
				# something went terribly wrong, retry
				debug("remote:buy", "...worked perfectly wrong")
				LCD.message_on(**MSG_BUY_RETRY)
				time.sleep(MSG_BUY_RETRY_WAIT)
		except requests.ConnectionError:
			debug("remote:buy", "connection refused. Are you online")
			LCD.message_on(**MSG_BUY_RETRY)
			time.sleep(MSG_BUY_RETRY_WAIT)
