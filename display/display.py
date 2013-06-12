#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import sys
import Image


SCREEN_PATH = path.join(path.dirname(path.realpath(__file__)), 'screen_base.png')
screen = None

def display_init():
	#try:
	screen = Image.open(SCREEN_PATH)
	#except:
	#	print("Error opening image file!")
	#	sys.exit()

	if not screen.size == (160,80) or not screen.mode == "1":
		print("Error: Wrong image size (%s , %s)" % (screen.size, screen.mode))
		sys.exit()

	screen.convert("1")

def display_mainview():
	pass

def display_name():
	pass

def diplay_price():
	pass

def display_idle():
	pass

def diplay_draw(image):
	pass