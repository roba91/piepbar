#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from display import Display

LCD = Display()

DEFAULT_AUTO_UPDATE_PERIOD = 120.0 # in seconds
FINISH_TIMEOUT = 25.0 # in seconds

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
	return {int(e['beverage']['id']): (str(e['beverage']['name']), float(e['beverage']['price'])) for e in json_data}


########################### interaction settings ###########################

MSG_UNKOWN_CODE = {'heading': 'Lern2Play', 'text': 'Nope, den Code gibts\n nicht. Echt nicht!'}
MSG_DECLINE = {'heading': 'Abbruch', 'text': 'Dann eben nicht.\nBeginne von vorn!'}
MSG_ACCEPT_NO_USER = {'heading': 'Stop! Fehler!', 'text': 'Wer kauft hier was?\nScanne deinen Namen.'}
MSG_ACCEPT_NO_PRODUCTS = {'heading': 'Stop! Fehler!', 'text': 'Nichts gekauft?\nGlaub ich nicht...'}
MSG_FUNC_USER_CHANGE = lambda name: {'heading': 'Oh hi %s' % name, 'text': "Didn't know it\n was you."}
MSG_UNKNOWN_PRODUCT = {'heading': 'Da fuq?', 'text': 'Was scannst du hier?\nAlter...'}
MSG_SYNC_ON = {'heading': 'Syncing...', 'text': 'Mach ma leisure,\ngeht gleich weiter.'}
MSG_SYNC_OFF = {'delay': 3} # you may define a minimal delay here
MSG_EXIT = {'heading': u'Ok tschöö...', 'text': 'Why? Why are you\ndoing this to me?'}
MSG_BUY_ON = lambda name: {'heading': str(name), 'text': "You're my favourite\ncustomer"}
MSG_BUY_OFF = {'delay': 3}