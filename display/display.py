#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import sys
import Image, ImageDraw, ImageFont
from displaydriver import DisplayDriver

base = None
screen = None
font = None
font_large = None
displaydriver = None

SCREEN_PATH = path.join(path.dirname(path.realpath(__file__)), 'screen_base.png')
FONT_PATH = path.join(path.dirname(path.realpath(__file__)), 'Terminus.ttf')
BOLDFONT_PATH = path.join(path.dirname(path.realpath(__file__)), 'TerminusBold.ttf')

def display_init():
	global screen, base, font, font_large, displaydriver

	try:
		base = Image.open(SCREEN_PATH)
	except:
		print("Error opening image file!")
		sys.exit()

	if not base.size == (160,80):
		print("Error: Wrong image size %s" % base.size)
		sys.exit()

	base = base.convert("1")
	screen = base.copy()

	try:
		displaydriver = DisplayDriver()
	except:
		print "Unable to open display"
		sys.exit()

def display_mainview():
	global screen
	screen = base.copy()
	draw = ImageDraw.Draw(screen)
	draw.text((10, 25), "OH HAI!", font=font)

	font = ImageFont.truetype(FONT_PATH, 14)
	font_large = ImageFont.truetype(BOLDFONT_PATH, 14)
	except:
		print("Error: loading font!")
		sys.exit()


def display_empty():
	display_name("")
	display_products("","")

def display_name(name):
	global screen
	draw = ImageDraw.Draw(screen)
	draw.rectangle(((0,0),(159,14)), fill=255)
	draw.line([(0,14),(159,14)], fill=0)
	draw.line([(0,16),(159,16)], fill=0)
	draw.text((1,1), name, font=font_large)

def display_products(drinks,sum):
	global screen
	draw = ImageDraw.Draw(screen)
	draw.rectangle(((0,17),(159,79)), fill=255)
	draw.line([(0,65),(159,65)], fill=0)
	draw.text([a-b for a,b in zip((158,82),font.getsize("Summe: %s" % sum))], "Summe: %s" % sum, font=font)

def display_idle():
	display_mainview()

def display_draw():
	screen.show()


