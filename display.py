#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import Image

screen = None

def display_init():
	#try:
	screen = Image.open("screen_base.tga")
	#except:
	#	print("Error opening image file!")
	#	sys.exit()

	if not screen.size() == (160,80) or not screen.mode() == "1":
		print("Error: Wrong image size (%s , %s)", screen.size())
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