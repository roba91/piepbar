#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import logging
import pygame
import time
from subprocess import Popen
from config import *

class Display(object):

	def __init__(self, idle_bg=IDLE_PATH, main_bg=MAIN_PATH, font=FONT_PATH,
				 font_size=14, bold_font=BOLD_PATH, bold_font_size=14):
	
		# Based on "Python GUI in Linux frame buffer"
		# http://www.karoltomala.com/blog/?p=679
		disp_no = os.getenv("DISPLAY")
	
		if disp_no:
			print "I'm running under X display = {0}".format(disp_no)
		# Check which frame buffer drivers are available
		# Start with fbcon since directfb hangs with composite output

		drivers = ['fbcon', 'directfb', 'svgalib']
		found = False
		for driver in drivers:
			# Make sure that SDL_VIDEODRIVER is set
			if not os.getenv('SDL_VIDEODRIVER'):
				os.putenv('SDL_VIDEODRIVER', driver)
			try:
				pygame.display.init()
			except pygame.error:
				print 'Driver: {0} failed.'.format(driver)
				continue
			found = True
			break

		if not found:
			raise Exception('No suitable video driver found!')
		
		self.size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
		self.unit = (self.size[0]/16, self.size[1]/16)
		print "Framebuffer self.size: %d x %d" % (self.size[0], self.size[1])
		print "Framebuffer self.unit: %d x %d" % (self.unit[0], self.unit[1])
		self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
		# Clear the screen to start
		self.screen.fill((0, 0, 0))
		# Initialise font support
		pygame.font.init()
		
		self.sfont = pygame.font.Font(FONT_PATH, 1*self.unit[1])
		self.lfont = pygame.font.Font(FONT_PATH, 2*self.unit[1])

		# Render the screen

		pygame.mouse.set_visible(False)


		pygame.display.update()

		red = (255, 0, 0)
		self.screen.fill(red)
		# Update the display
		pygame.display.update()

		#self.p = Popen(["mplayer", "-vo", "fbdev2", "-endpos", "00:00:10", MOVIE])

		self.bg = self._create_bg()
		self.idle_bg = self._create_idle_bg()

		self.playprocess = None

	def _draw(self):
		pygame.display.update()

	def _create_idle_bg(self):
		background = pygame.Surface(self.size)
		background.fill((0,0,0))
	
		for i in range(32):
			pygame.draw.line(background, (100,100,100), (0, i*self.unit[1]), (self.size[0], i*self.unit[1]))
			pygame.draw.line(background, (100,100,100), (i*self.unit[0], 0), (i*self.unit[0], self.size[1]))

		text = self.lfont.render("Ready!", True, (255,255,255))
		background.blit(text, (3*self.unit[0], 14*self.unit[1]))
		text = self.sfont.render("Scan code to", True, (255,255,255))
		background.blit(text, (8*self.unit[0], 14*self.unit[1]))
		text = self.sfont.render("begin purchase.", True, (255,255,255))
		background.blit(text, (9*self.unit[0], 15*self.unit[1]))

		background.convert()

		return background

	def _create_bg(self):
		background = pygame.Surface(self.size)
		background.fill((0,0,0))
	
		for i in range(32):
			pygame.draw.line(background, (100,100,100), (0, i*self.unit[1]), (self.size[0], i*self.unit[1]))
			pygame.draw.line(background, (100,100,100), (i*self.unit[0], 0), (i*self.unit[0], self.size[1]))

		pygame.draw.line(background, (255,255,255), (0, 2*self.unit[1]), (15*self.unit[0], 2*self.unit[1]), 2)
		pygame.draw.line(background, (255,255,255), (0, 2*self.unit[1]+self.unit[1]/10), (15*self.unit[0]+self.unit[0]/10, 2*self.unit[1]+self.unit[1]/10), 2)

		pygame.draw.line(background, (255,255,255), (11*self.unit[0], 14*self.unit[1]), (16*self.unit[0], 14*self.unit[1]), 2)
		pygame.draw.line(background, (255,255,255), (11*self.unit[0]+self.unit[0]/10, 14*self.unit[1]+self.unit[1]/10), (16*self.unit[0]+self.unit[0]/10, 14*self.unit[1]+self.unit[1]/10), 2)


		background.convert()

		return background

	def _stop_video(self):
		if self.playprocess:
			if not self.playprocess.poll():
				self.playprocess.kill()

	def _start_video(self):
		self._stop_video()
		self.playprocess = Popen(["mplayer", "-vo", "fbdev2", "-geometry", "0:0", "-endpos", "00:00:10", MOVIE])

	def idle(self):
		self.screen.blit(self.bg, (0,0))	
		self._draw()

		self._start_video()
		time.sleep(5)
		self._stop_video()

	def update(self, name=None, drinks=None, total=0):
		if name:
			text = self.lfont.render(name, True, (255,255,255))
			self.screen.blit(text, (0,0))

		for i in range(3,14):
			text = self.sfont.render("10.00", True, (255,255,255))
			self.screen.blit(text, (13*self.unit[0], i*self.unit[1]))

		self._draw()

	def message(self, text, heading=None , delay=DEFAULT_MESSAGE_DELAY, align=DEFAULT_MESSAGE_ALIGN):
		pass

	def message_on(self, text, heading=None, align=DEFAULT_MESSAGE_ALIGN, delay=None):
		pass

	def message_off(self, delay=None):
		pass

