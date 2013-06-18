#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import threading
from product_list import PRODUCT_LIST
from config import *
from remote import buy

products = [] # list: int
user = None # string
timer = None

############################### special actions ###############################
def shutdown():
	LCD.message(**MSG_EXIT)
	sys.exit()

def sync():
	LCD.message_on(**MSG_SYNC_ON)
	success = PRODUCT_LIST.update()
	time.sleep(MSG_SYNC_DELAY)
	if success: LCD.message(**MSG_SYNC_SUCCESS)
	else: LCD.message(**MSG_SYNC_FAILED)

def auto_sync():
	# this is harpooning automagically during idle time - do not display anything
	PRODUCT_LIST.update()

############################### finish purchase ###############################
def accept():
	stop_timer()
	if not user:
		LCD.message(**MSG_ACCEPT_NO_USER)
	elif not products:
		LCD.message(**MSG_ACCEPT_NO_PRODUCTS)
	else:
		LCD.message_on(**MSG_BUY_ON(user))
		buy(user, *products)
		reset()
		LCD.message_off(**MSG_BUY_OFF)
		print ">>>>>>>>>>>>> fin accept"

def decline():
	stop_timer()
	LCD.message(**MSG_DECLINE)
	reset()

def timeout():
	# accept as purchase
	if not user and not products:
		# the purchase was already handled -> should happen rarely
		pass
	elif not user or not products:
		# no valid purchase -> decline
		decline()
	else:
		accept()

def reset():
	global user, products
	stop_timer()
	needs_release = products or user
	products = []
	user = []
	LCD.idle()
	PRODUCT_LIST.idle.set()

################################ do purchasing ################################
def start_timer():
	global timer
	if timer:
		timer.cancel()
	timer = threading.Timer(FINISH_TIMEOUT, timeout)
	timer.setDaemon(True)
	timer.start()

def stop_timer():
	if timer:
		timer.cancel()

def update_display():
	drinks = [(PRODUCT_LIST.get_name(pid), PRODUCT_LIST.get_price(pid)) for pid in products]
	total = sum([PRODUCT_LIST.get_price(pid) for pid in products])
	LCD.update(user, drinks, total)

def user_code(scanned_user):
	global user
	stop_timer()
	PRODUCT_LIST.idle.clear()
	if user and user != scanned_user:
		LCD.message(**MSG_FUNC_USER_CHANGE(scanned_user))
	user = scanned_user
	start_timer()
	update_display()

def product_code(product_id):
	global products
	stop_timer()
	PRODUCT_LIST.idle.clear()
	try:
		# don't let fools run the system into malicious states -> check cast
		product_id = int(product_id)
	except ValueError:
		product_id = None
	if not product_id or not PRODUCT_LIST.contains(product_id):
		LCD.message(**MSG_UNKNOWN_PRODUCT)
	else:
		products.append(product_id)
		start_timer()
		update_display()

################################ handle input #################################
ACTIONS = {
	CODE_FORCE_EXIT: shutdown,
	CODE_FORCE_SYNC: sync,
	CODE_DECLINE: decline,
	CODE_ACCEPT: accept,
}

def handle_input(code):
	if code in ACTIONS:
		ACTIONS[code]()
	elif code.startswith(CODE_PREFIX_USER):
		user_code(code.replace(CODE_PREFIX_USER, "", 1))
	elif code.startswith(CODE_PREFIX_PRODUCT):
		product_code(code.replace(CODE_PREFIX_PRODUCT, "", 1))
	else:
		LCD.message(**MSG_UNKOWN_CODE)

