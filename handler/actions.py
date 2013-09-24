#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import threading
import logging
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
	logger = logging.getLogger("actions:sync")
	logger.info("syncing...")
	LCD.message_on(**MSG_SYNC_ON)
	success = PRODUCT_LIST.update()
	time.sleep(MSG_SYNC_DELAY)
	if success:
		LCD.message(**MSG_SYNC_SUCCESS)
		logger.info("sync successful")
	else:
		LCD.message(**MSG_SYNC_FAILED)
		logger.error("sync failed")

def auto_sync():
	logger = logging.getLogger("actions:auto_sync")
	logger.info("cowardly syncing...")
	# this is harpooning automagically during idle time - do not display anything
	PRODUCT_LIST.update()

############################### finish purchase ###############################
def accept():
	logger = logging.getLogger("actions:accept")
	stop_timer()
	if not user:
		logger.info("no user specified")
		beep()
		LCD.message(**MSG_ACCEPT_NO_USER)
	elif not products:
		logger.info("no products specified")
		beep()
		LCD.message(**MSG_ACCEPT_NO_PRODUCTS)
	else:
		logger.info("buying...")
		# message_on() and reset() redraw the screen -> MSG_BUY_ON shown twice
		LCD.message_on(**MSG_BUY_ON(user))
		success = buy(user, *products)

		if success:
			logger.info("buying successful")
		else:
			logger.error("buying failed")
			# display error message -> nothing purchased
			LCD.message_on(**MSG_BUY_FAILED)
		reset()
		LCD.message_off(**MSG_BUY_OFF)

def decline():
	logger = logging.getLogger("actions:decline")
	logger.info("decline")
	stop_timer()
	beep()
	LCD.message(**MSG_DECLINE)
	reset()

def undo_last_selection():
	logger = logging.getLogger("actions:undo_last_selection")
	logger.info("undoing")
	global products
	stop_timer()
	products = products[:-1]
	start_timer()
	update_display()


def timeout():
	logger = logging.getLogger("actions:timeout")
	logger.warning("timeouted...")
	# accept as purchase
	if not user and not products:
		# the purchase was already handled -> should happen rarely
		logger.warning("...doing nothing")
		pass
	elif not user or not products:
		# no valid purchase -> decline
		logger.warning("...declining")
		decline()
	else:
		logging.warning("...accepting")
		accept()

def reset():
	logger = logging.getLogger("actions:reset")
	logger.info("resetting $stuff")
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
	logger = logging.getLogger("actions:update_display")
	logger.info("updating with...")
	drinks = [(PRODUCT_LIST.get_name(pid), PRODUCT_LIST.get_price(pid)) for pid in products]
	logger.info("...drinks: %s" % str(drinks))
	total = sum([PRODUCT_LIST.get_price(pid) for pid in products])
	logger.info("...total: %.2f" % total)
	LCD.update(user, drinks, total)

def user_code(scanned_user):
	logger = logging.getLogger("actions:user_code")
	# if the user is allowed to buy things is checked by the intranet
	global user
	stop_timer()
	PRODUCT_LIST.idle.clear()
	logger.info("scanned user: %s" % scanned_user)
	if user and user != scanned_user:
		beep()
		LCD.message(**MSG_FUNC_USER_CHANGE(scanned_user))
	user = scanned_user
	start_timer()
	update_display()

def product_code(product_id):
	logger = logging.getLogger("actions:product_code")
	global products
	stop_timer()
	PRODUCT_LIST.idle.clear()
	logger.info("scanned product: %s" % product_id)
	try:
		# don't let fools run the system into malicious states -> check cast
		product_id = int(product_id)
	except ValueError:
		product_id = None
		logger.critical("product code invalid (no int)")
	if not product_id or not PRODUCT_LIST.contains(product_id):
		logger.error("product code unknown")
		LCD.message(**MSG_UNKNOWN_PRODUCT)
	else:
		products.append(product_id)
		logger.info("product accepted, new list: %s" % str(products))
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
	logger = logging.getLogger("actions:handle_input")
	logger.debug("Scanned code: %s" % code)
	if code in ACTIONS:
		ACTIONS[code]()
	elif code.startswith(CODE_PREFIX_USER):
		user_code(code.replace(CODE_PREFIX_USER, "", 1))
	elif code.startswith(CODE_PREFIX_PRODUCT):
		product_code(code.replace(CODE_PREFIX_PRODUCT, "", 1))
	else:
		logger.error("unknown command")
		beep()
		LCD.message(**MSG_UNKOWN_CODE)

