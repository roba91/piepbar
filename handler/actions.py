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
	debug("actions:sync", "syncing...")
	LCD.message_on(**MSG_SYNC_ON)
	success = PRODUCT_LIST.update()
	time.sleep(MSG_SYNC_DELAY)
	debug("actions:sync", "sync %s" % "successful" if success else "failed")
	if success: LCD.message(**MSG_SYNC_SUCCESS)
	else: LCD.message(**MSG_SYNC_FAILED)

def auto_sync():
	debug("actions:auto_sync", "cowardly syncing...")
	# this is harpooning automagically during idle time - do not display anything
	PRODUCT_LIST.update()

############################### finish purchase ###############################
def accept():
	stop_timer()
	if not user:
		debug("actions:accept", "no user specified")
		beep()
		LCD.message(**MSG_ACCEPT_NO_USER)
	elif not products:
		debug("actions:accept", "no products specified")
		beep()
		LCD.message(**MSG_ACCEPT_NO_PRODUCTS)
	else:
		debug("actions:accept", "buying...")
		# message_on() and reset() redraw the screen -> MSG_BUY_ON shown twice
		LCD.message_on(**MSG_BUY_ON(user))
		success = buy(user, *products)
		debug("actions:accept", "buying %s" % "successful" if success else "failed")
		if not success:
			# display error message -> nothing purchased
			LCD.message_on(**MSG_BUY_FAILED)
		reset()
		LCD.message_off(**MSG_BUY_OFF)

def decline():
	debug("actions:decline", "decline")
	stop_timer()
	beep()
	LCD.message(**MSG_DECLINE)
	reset()

def undo_last_selection():
	debug("actions:undo_last_selection", "undoing")
	global products
	stop_timer()
	products = products[:-1]
	start_timer()
	update_display()


def timeout():
	debug("actions:timeout", "timeouted...")
	# accept as purchase
	if not user and not products:
		# the purchase was already handled -> should happen rarely
		debug("actions:decline", "...doing nothing")
		pass
	elif not user or not products:
		# no valid purchase -> decline
		debug("actions:decline", "...declining")
		decline()
	else:
		debug("actions:decline", "...accepting")
		accept()

def reset():
	debug("actions:reset", "resetting $stuff")
	global user, products
	stop_timer()
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
	debug("actions:update_display", "updating with...")
	drinks = [(PRODUCT_LIST.get_name(pid), PRODUCT_LIST.get_price(pid)) for pid in products]
	debug("actions:update_display", "...drinks: %s" % str(drinks))
	total = sum([PRODUCT_LIST.get_price(pid) for pid in products])
	debug("actions:update_display", "...total: %.2f" % total)
	LCD.update(user, drinks, total)

def user_code(scanned_user):
	# if the user is allowed to buy things is checked by the intranet
	global user
	stop_timer()
	PRODUCT_LIST.idle.clear()
	debug("actions:user_code", "scanned user: %s" % user)
	if user and user != scanned_user:
		beep()
		LCD.message(**MSG_FUNC_USER_CHANGE(scanned_user))
	user = scanned_user
	start_timer()
	update_display()

def product_code(product_id):
	global products
	stop_timer()
	PRODUCT_LIST.idle.clear()
	debug("actions:product_code", "scanned product: %s" % product_id)
	try:
		# don't let fools run the system into malicious states -> check cast
		product_id = int(product_id)
	except ValueError:
		product_id = None
		debug("actions:product_code", "product code invalid (no int)")
	if not product_id or not PRODUCT_LIST.contains(product_id):
		debug("actions:product_code", "product code unknown")
		LCD.message(**MSG_UNKNOWN_PRODUCT)
	else:
		products.append(product_id)
		debug("actions:product_code", "product accepted, new list: %s" % str(products))
		start_timer()
		update_display()

################################ handle input #################################
ACTIONS = {
	CODE_FORCE_EXIT: shutdown,
	CODE_FORCE_SYNC: sync,
	CODE_DECLINE: decline,
	CODE_ACCEPT: accept,
	CODE_UNDO: undo_last_selection,
}

def handle_input(code):
	if code in ACTIONS:
		ACTIONS[code]()
	elif code.startswith(CODE_PREFIX_USER):
		user_code(code.replace(CODE_PREFIX_USER, "", 1))
	elif code.startswith(CODE_PREFIX_PRODUCT):
		product_code(code.replace(CODE_PREFIX_PRODUCT, "", 1))
	else:
		debug("actions:handle_input", "unknown command")
		beep()
		LCD.message(**MSG_UNKOWN_CODE)

