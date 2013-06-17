#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import threading
from config import *
from actions import shutdown, handle_input, sync

def scanner():
	LCD.idle()
	while True:
		try:
			handle_input(raw_input())
		except KeyboardInterrupt:
			handle_interrupt()

def handle_interrupt():
	print "\n>>> Fools, don't let them escape! <<<\n"
	sys.exit(0) # for testing reasons

def auto_update(update_period=DEFAULT_AUTO_UPDATE_PERIOD):
	def auto_sync(update_period, *args, **kwargs):
		while True:
			time.sleep(update_period)
			sync()
	thread = threading.Thread(target=auto_sync, args=[update_period])
	thread.setDaemon(True)
	thread.start()