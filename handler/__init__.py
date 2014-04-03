#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import threading
from config import *
from actions import shutdown, handle_input, auto_sync

import pygame

def scanner():
	LCD.idle()
	LCD.update(name = "Penis Ulrich")

	input = ""
	while True:

		'''
		try:
			handle_input(raw_input())
		except KeyboardInterrupt:
			handle_interrupt()

		'''
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				handle_interrupt()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					handle_interrupt()
				elif event.unicode == '\r':
					input += event.unicode
					handle_input(input)
					input = ""
				else:
					input += event.unicode

def handle_interrupt():
	print "\n>>> Fools, don't let them escape! <<<\n"
	sys.exit(0) # for testing reasons

def auto_update(update_period=DEFAULT_AUTO_UPDATE_PERIOD):
	def run_background(update_period, *args, **kwargs):
		while True:
			time.sleep(update_period)
			auto_sync()
	thread = threading.Thread(target=run_background, args=[update_period])
	thread.setDaemon(True)
	thread.start()