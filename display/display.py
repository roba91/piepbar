#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import sys
import threading
import time
import Image, ImageDraw, ImageFont
from displaydriver import DisplayDriver


IDLE_PATH = path.join(path.dirname(path.realpath(__file__)), 'idle_bg.png')
MAIN_PATH = path.join(path.dirname(path.realpath(__file__)), 'main_bg.png')

FONT_PATH = path.join(path.dirname(path.realpath(__file__)), 'Terminus.ttf')
BOLD_PATH = path.join(path.dirname(path.realpath(__file__)), 'TerminusBold.ttf')

DUMMY_DISPLAY = True # Set to false to use the real hardware

class Display(object):

	def __init__(self, idle_bg=IDLE_PATH, main_bg=MAIN_PATH, font=FONT_PATH,
				 font_size=14, bold_font=BOLD_PATH, bold_font_size=14):

		if main_bg:
			try:
				self._main_bg = Image.open(main_bg)
			except:
				print"Error opening image file!"
				sys.exit()

			if not self._main_bg.size == (160,80):
				print"Error: Wrong image size %s" % self._main_bg.size
				sys.exit()

			self._main_bg = self._main_bg.convert('1')
		else:
			self._main_bg = Image.new('1', (160,80), 255)

		if idle_bg:
			try:
				self._idle_bg = Image.open(idle_bg)
			except:
				print"Error opening image file!"
				sys.exit()

			if not self._idle_bg.size == (160,80):
				print"Error: Wrong image size %s" % self._idle_bg.size
				sys.exit()

			self._idle_bg = self._idle_bg.convert('1')
		else:
			self._idle_bg = Image.new('1', (160,80), 255)

		if font:
			try:
				self._font = ImageFont.truetype(font, font_size)
			except:
				print"Error: loading font!"
				sys.exit()

		if bold_font:
			try:
				self._bold_font = ImageFont.truetype(bold_font, bold_font_size)
			except:
				print"Error: loading bold font!"
				sys.exit()
		
		try:
			self._displaydriver = DisplayDriver(dummy=DUMMY_DISPLAY)
		except:
			print "Error: Unable to open display!"
			sys.exit()

		self._screen = self._idle_bg.copy()
		self._was_idle = True

		self._viewmsg = False
		self._msglock = threading.Lock()
		self._msgscreen = Image.new('1', (160,80), 255)

	def _draw(self):
		self._msglock.acquire()
		if self._viewmsg:
			self._displaydriver.send_image(self._msgscreen)
		else:
			self._displaydriver.send_image(self._screen)
		self._msglock.release()

	def idle(self):
		self._screen = self._idle_bg.copy()
		self._was_idle = True
		self._draw()

	def update(self, name=None, drinks=None, total=None):
		if self._was_idle:
			self._screen = self._main_bg.copy()
			self._was_idle = False
		
		draw = ImageDraw.Draw(self._screen)

		if name:
			draw.rectangle([0,0,159,13],fill=255)
			draw.text((1,1),name,font=self._bold_font)

		if drinks:
			draw.rectangle([0,17,159,65],fill=255)

			y = 53
			for drink in drinks[:-5:-1]:
				if len(drinks)>4 and drink == drinks[-4]:
					draw.text((1,17),"und noch %s mehr..." % (len(drinks)-3),font=self._font)
				else:
					size = self._font.getsize("%.2f" % drink[1])
					draw.text((156-size[0],y),"%.2f" % drink[1],font=self._font)
					draw.text((1,y),drink[0],font=self._font)
				y=y-12

		if total:
			size = self._font.getsize("Summe: %.2f" % total)
			draw.rectangle([0,67,159,79],fill=255)
			draw.text((156-size[0],68),"Summe: %.2f" % total,font=self._bold_font)

		self._draw()

	def message(self, text, delay=2):
		#TODO delay
		self._msgscreen = self._screen.copy()
		draw = ImageDraw.Draw(self._msgscreen)

		size = self._font.getsize(text)

		textmargin = [
			((160-size[0])//2-2,
			(80-size[1])//2-2),
			((160-size[0])//2+size[0]+2,
			(80-size[1])//2+size[1]+2),
		]

		draw.rectangle(textmargin,outline=0,fill=255)
		draw.text((textmargin[0][0]+2,textmargin[0][1]+2),text,font=self._font)
		
		self._viewmsg = True

		self._draw()


	

