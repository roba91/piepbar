#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import threading
from config import *
from actions import shutdown, handle_input, auto_sync

def auto_update(update_period=DEFAULT_AUTO_UPDATE_PERIOD):
	def run_background(update_period, *args, **kwargs):
		while True:
			time.sleep(update_period)
			auto_sync()
	thread = threading.Thread(target=run_background, args=[update_period])
	thread.setDaemon(True)
	thread.start()