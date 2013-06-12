#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from communication import get_remote_prices as get_new_prices
from communication import add_bill as buy_products


def handle_scanning():
	print "Started..."
	while True:
		try:
			handle_input(raw_input())
		except KeyboardInterrupt:
			handle_interrupt()

def handle_interrupt():
	print ">>> Fools, don't let them escape! <<<"
	sys.exit(0) # for testing reasons

################ define special actions ################
def reload_prices():
	print "Fetching new price list..."
	remote = get_new_prices()
	if not remote:
		# TODO: @display
		print "--> Fetching failed!"
	else:
		# TODO: @display
		print "--> Prices updated!"

def shutdown():
	# TODO: @display
	print "Shutting down..."
	sys.exit()

SPECIAL_ACTIONS = {
	'__FORCE_RELOAD__': reload_prices,
	'__FORCE_EXIT__': shutdown,
}

################# default buy work flow #################
PURCHASE_ACCEPT = '__ACCEPT__'
PURCHASE_DECLINE = '__DECLINE__'
USER_PREFIX = 'USER__'
PRODUCT_PREFIX = 'PRODUCT__'
prices = {}
products = []
user = None

def handle_input(code):
	if code in SPECIAL_ACTIONS:
		SPECIAL_ACTIONS[code]()
	else:
		handle_code(code)

def handle_code(code):
	if code == PURCHASE_ACCEPT: handle_accept()
	elif code == PURCHASE_DECLINE: handle_decline()
	elif code.startswith(USER_PREFIX): handle_user_code(code)
	elif code.startswith(PRODUCT_PREFIX): handle_product_code(code)
	else: handle_unknown_code(code)

def to_initial_state():
	products = []
	user = []

def handle_accept():
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
	scanned_user = code.replace(USER_PREFIX, "", 1)
	if user and user != scanned_user:
		# TODO: @display
		# TODO: warn user -> do not abort, last scanned user is buyer
		print ">>> User updated!"
	user = scanned_user
	print ">>> scanned user: %s" % user

def handle_product_code(code):
	# TODO: @display
	new_product = code.replace(PRODUCT_PREFIX, "", 1)
	products.add(new_product)

def handle_unknown_code(code=None):
	pass
