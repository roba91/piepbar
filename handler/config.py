#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from collections import Counter

DEBUG = True

DEFAULT_AUTO_UPDATE_PERIOD = 120.0 # in seconds
FINISH_TIMEOUT = 25.0 # in seconds
DEFAULT_MESSAGE_DELAY = 3

CODE_FORCE_EXIT = '__exit' # TODO: use more save code?
CODE_FORCE_SYNC = '__sync' # TODO: use more save code?

CODE_DECLINE = '__decline'
CODE_ACCEPT = '__accept'

CODE_UNDO = '__undo' # undo last item selection

CODE_PREFIX_USER = 'user__'
CODE_PREFIX_PRODUCT = 'item__'

URL_BASE = ''
URL_SYNC = URL_BASE + 'api/items.json'
URL_BUY = URL_BASE + 'api/buy'
URL_USER = URL_BASE + 'api/user'

AUTH_USER = 'user'
AUTH_PASSWORD = 'password'

def encode_buy(products):
	# {prod_id: amount}
	return Counter(products)

def decode_product_list(json_data):
	# convert json_data to {data: (name, price, image_url)} dict
	return {int(e['id']): (e['name'], float(e['price']), URL_BASE + e['image_urls']['small']) for e in json_data}


############################# logging settings #############################

LOG_FILE = "piepbar.log"
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s %(levelname)s [%(name)s] %(message)s'
LOG_DATEFORMAT = '%d-%m-%Y %H:%M:%S'

########################### interaction settings ###########################

MSG_UNKOWN_CODE = {'heading': 'Lern2Play', 'text': 'Nope, den Code gibts\n nicht. Echt nicht!'}
MSG_DECLINE = {'heading': 'Abbruch', 'text': 'Dann eben nicht.\nBeginne von vorn!'}
MSG_ACCEPT_NO_USER = {'heading': 'Stop! Fehler!', 'text': 'Wer kauft hier was?\nScanne deinen Namen.'}
MSG_ACCEPT_NO_PRODUCTS = {'heading': 'Stop! Fehler!', 'text': 'Nichts gekauft?\nGlaub ich nicht...'}
MSG_FUNC_USER_CHANGE = lambda name: {'heading': 'Oh hi %s' % name, 'text': "Didn't know it\n was you."}
MSG_UNKNOWN_USER = {'heading': 'Wer?', 'text': 'Dich kenn ich nich!'}
MSG_USER_BLOCKED = {'heading': 'Halt stopp!', 'text': 'Du bist gesperrt!\nZahle zuerst deine Schulden.'}
MSG_UNKNOWN_PRODUCT = {'heading': 'Da fuq?', 'text': 'Was scannst du hier?\nAlter...'}
MSG_SYNC_ON = {'heading': 'Syncing...', 'text': 'Mach ma leisure,\ngeht gleich weiter.'}
MSG_SYNC_DELAY = DEFAULT_MESSAGE_DELAY
MSG_EXIT = {'heading': u'Ok tschöö...', 'text': 'Why? Why are you\ndoing this to me?'}
MSG_BUY_ON = lambda name: {'heading': str(name), 'text': "You're my favourite\ncustomer", 'delay': 2}
MSG_BUY_OFF = {'delay': 2} # need a delay -> dunno why
MSG_BUY_RETRY = {'heading': 'Retrying...', 'text': 'Wiederhole Vorgang.\nIntranet down?'}
MSG_BUY_RETRY_WAIT = 10
MSG_BUY_FAILED = {'heading': 'Nope, dude!', 'text': 'Du kannst nichts\nkaufen. Zumindest im\nMoment. Hello IT?', 'delay': DEFAULT_MESSAGE_DELAY}
MSG_SYNC_SUCCESS = {'heading': 'Sync ok', 'text': u'Getränke sind wieder\nup to date'}
MSG_SYNC_FAILED = {'heading': 'Sync failed', 'text': 'Irgendwas ist schief\ngelaufen'}


################################### beep ###################################

def beep():
	print '\a'
