#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import Image, ImageDraw, ImageFont

base = None
screen = None
font = ImageFont.truetype("LCD.ttf", 12) #TODO move to init

def display_init():
	global screen, base

	try:
		base = Image.open("screen_base.png")
	except:
		print("Error opening image file!")
		sys.exit()

	if not base.size == (160,80):
		print("Error: Wrong image size %s" % base.size)
		sys.exit()

	base = base.convert("1")
	screen = base.copy()

def display_mainview():
	global screen
	screen = base.copy()
	draw = ImageDraw.Draw(screen)
	draw.text((10, 25), "OH HAI!", font=font)

	display_draw()

def display_name(name):
	pass

def diplay_add_drink(drink, price):
	pass

def display_idle():
	display_mainview()

def display_draw():
	screen.show()


