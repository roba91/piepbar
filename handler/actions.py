#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import threading
from product_list import PRODUCT_LIST
from config import *
from remote import buy

products = [] # list: int
user = None # string
num_locks = 0 # int
timer = None

############################### special actions ###############################
def shutdown():
	print ">>> Exiting" # TODO: @display
	sys.exit()

def sync():
	print ">>> Syncing" # TODO: @display
	PRODUCT_LIST.update()

############################### finish purchase ###############################
def accept():
	if not user:
		print ">>> no user specified" # TODO: @display
	elif not products:
		print ">>> no products selected" # TODO: @display
	else:
		print ">>> buying products for %s: %s" % (user, products) # TODO: @display
		buy(user, *products)
		reset()

def timeout():
	# accept as purchase
	print ">>> timeout"
	if not user or not products:
		# no valid purchase -> decline
		decline()
	else:
		accept()

def decline():
	print ">>> purchase aborted" # TODO: @display
	reset()

def reset():
	global user, products, num_locks
	needs_release = products or user
	products = []
	user = []
	# release all but one lock, then reset the number of locks, and release the lock finally
	for i in range(max(num_locks-1,0)):
		PRODUCT_LIST.lock.release()
	num_locks = 0
	# only if the recursion level of the RLock is zero, the lock is released
	if needs_release: PRODUCT_LIST.lock.release()

################################ do purchasing ################################
def acquire_lock():
	global num_locks
	PRODUCT_LIST.lock.acquire()
	num_locks += 1

def start_timer():
	global timer
	if timer:
		timer.cancel()
	timer = threading.Timer(FINISH_TIMEOUT, timeout)
	timer.start()

def user_code(scanned_user):
	global user, num_locks
	acquire_lock()
	if user and user != scanned_user:
		print ">>> User updated!" # TODO: @display (warn, no abort)
	user = scanned_user
	start_timer()
	print ">>> scanned user: %s" % user # TODO: @display

def product_code(product_id):
	global products, num_locks
	acquire_lock()
	new_product = int(product_id)
	products.append(new_product)
	start_timer()
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

