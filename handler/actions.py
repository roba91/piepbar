#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from product_list import PRODUCT_LIST
from config import *
from remote import buy

products = [] # list: int
user = None # string
num_locks = 0 # int

############################### special actions ###############################
def shutdown():
	print ">>> Exiting" # TODO: @display
	sys.exit()

def sync():
	print ">>> Syncing" # TODO: @display
	PRODUCT_LIST.update()

############################### finish purchase ###############################
def accept():
	global user, products
	print ">>> buying products for %s: %s" % (user, products) # TODO: @display
	buy(user, *products)
	reset()

def decline():
	print ">>> purchase aborted" # TODO: @display
	reset()

def reset():
	global user, products, num_locks
	products = []
	user = []
	# release all but one lock, then reset the number of locks, and release the lock finally
	for i in range(max(num_locks-1,0)): PRODUCT_LIST.lock.release()
	num_locks = 0
	# only if the recursion level of the RLock is zero, the lock is released
	PRODUCT_LIST.lock.release()

################################ do purchasing ################################
def acquire_lock():
	global num_locks
	PRODUCT_LIST.lock.acquire()
	num_locks += 1

def user_code(scanned_user):
	global user, num_locks
	acquire_lock()
	if user and user != scanned_user:
		print ">>> User updated!" # TODO: @display (warn, no abort)
	user = scanned_user
	print ">>> scanned user: %s" % user # TODO: @display

def product_code(product_id):
	global products, num_locks
	acquire_lock()
	new_product = int(product_id)
	products.append(new_product)
	print ">>> scanned product: %s" % new_product # TODO: @display

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
		print "Unknown code scanned!" # TODO: @display

