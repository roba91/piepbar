#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter


DEFAULT_AUTO_UPDATE_PERIOD = 30.0 # in seconds
FINISH_TIMEOUT = 15.0 # in seconds

CODE_FORCE_EXIT = "_exit"
CODE_FORCE_SYNC = "_sync"

CODE_DECLINE = "_nope"
CODE_ACCEPT = "_ok"

CODE_PREFIX_USER = "user__"
CODE_PREFIX_PRODUCT = "prod__"

URL_SYNC = "http://localhost:3000/getraenke.json"
URL_BUY = "http://localhost:3000/rechnungen/buy"
AUTH_USER = "user"
AUTH_PASSWORD = "password"

def encode_buy(products):
	# {prod_id: amount}
	return Counter(products)

def decode_product_list(json_data):
	# convert json_data to {data: (name, price)} dict
	return {int(e['beverage']['id']): (str(e['beverage']['name']), str(e['beverage']['price'])) for e in json_data}