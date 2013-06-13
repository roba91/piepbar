#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: regular auto-sync
# TODO: timeout for __ACCEPT__

import sys
import time
import threading
from communication import sync as sync_with_intranet
from communication import add_bill as buy_products

AUTO_UPDATE_PERIOD = 60.0 # in seconds

def handle_scanning():
	sync()
	while True:
		try:
			handle_input(raw_input())
		except KeyboardInterrupt:
			handle_interrupt()

def handle_interrupt():
	print "\n>>> Fools, don't let them escape! <<<\n"
	sys.exit(0) # for testing reasons

def auto_update():
	def auto_sync():
		while True:
			time.sleep(AUTO_UPDATE_PERIOD)
			sync()
	thread = threading.Thread(target=auto_sync)
	thread.setDaemon(True)
	thread.start()


################ define special actions ################
# special actions are do not acquire a lock by default #
def sync():
	with LOCK:
		global prices, names
		#TODO: @display
		print "Synchronizing..."
		remote_prices, remote_names = sync_with_intranet()
		if not remote_prices or not remote_names:
			# TODO: @display
			print "--> Fetching failed!"
		else:
			# TODO: @display
			prices = remote_prices
			names = remote_names
			print "--> Synchronized!"

def shutdown():
	# TODO: @display
	print "Shutting down..."
	sys.exit()

SPECIAL_ACTIONS = {
	'__FORCE_SYNC__': sync,
	'__FORCE_EXIT__': shutdown,
}


################# default buy work flow #################
### all common purchase actions acquire a lock first ####
PURCHASE_ACCEPT = '__ACCEPT__'
PURCHASE_DECLINE = '__DECLINE__'
USER_PREFIX = 'USER__'
PRODUCT_PREFIX = 'PRODUCT__'
LOCK = threading.Lock()
names = {} # dict[obj_id: name] -> int x string
prices = {} # dict[obj_id: price] -> int x number
products = [] # list: int
user = None # string

def handle_input(code):
	if code in SPECIAL_ACTIONS:
		SPECIAL_ACTIONS[code]()
	else:
		LOCK.acquire() # TODO: ensure that the lock is released in ANY case!
		handle_code(code)

def handle_code(code):
	if code == PURCHASE_ACCEPT: handle_accept()
	elif code == PURCHASE_DECLINE: handle_decline()
	elif code.startswith(USER_PREFIX): handle_user_code(code)
	elif code.startswith(PRODUCT_PREFIX): handle_product_code(code)
	else: handle_unknown_code(code)

def to_initial_state():
	global user, products
	products = []
	user = []
	LOCK.release()

def handle_accept():
	global user, products
	# TODO: @display
	print ">>> buying products for %s: %s" % (user, products)
	buy_products(user, *products)
	to_initial_state()

def handle_decline():
	# TODO: @display
	print ">>> purchase aborted"
	to_initial_state()
	pass

def handle_user_code(code):
	global user
	scanned_user = code.replace(USER_PREFIX, "", 1)
	if user and user != scanned_user:
		# TODO: @display
		# TODO: warn user -> do not abort, last scanned user is buyer
		print ">>> User updated!"
	user = scanned_user
	print ">>> scanned user: %s" % user

def handle_product_code(code):
	global products
	# TODO: @display
	new_product = int(code.replace(PRODUCT_PREFIX, "", 1))
	products.append(new_product)
	print ">>> scanned product: %s" % new_product

def handle_unknown_code(code=None):
	pass


