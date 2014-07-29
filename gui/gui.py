#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import logging
from config import *
from textrect import *

import pygame
from pygame.locals import *


class Gui(object):

	def __init__(self, screen):

		self.logger = logging.getLogger("gui")

		self._screen = screen
		if self._screen == None:
			self.logger.critical("Gui needs screen")
			sys.exit()

		self._res_x = screen.get_width()
		self._res_y = screen.get_height()
		self._x_unit = self._res_x/10
		self._y_unit = self._res_y/16

		self._text_fg_color = Color('white')
		self._text_bg_color = Color('grey')

		self._idle_surface = pygame.image.load(IDLE_PATH)
		self._idle_surface.convert()
		self._idle_surface = pygame.transform.scale(self._idle_surface, (self._res_x, self._res_y))

		self._font = pygame.font.Font(FONT_PATH, 72)
		self._message_font = pygame.font.Font(FONT_PATH, 21)
		self._message_head_font = pygame.font.Font(FONT_PATH, 27)

		self._message_bg = pygame.image.load(MESSAGE_PATH)
		self._message_bg.convert()
		self._message_bg = pygame.transform.scale(self._message_bg, (self._res_x, self._res_y))
		self._message_surf = self._message_bg.copy()

		self._main_bg = pygame.image.load(MAIN_PATH)
		self._main_bg.convert()
		self._main_bg = pygame.transform.scale(self._main_bg, (self._res_x, self._res_y))
		self._main_surface = self._main_bg.copy()

		self._viewmsg = False

	def _draw(self):
		self._screen.blit(self._main_surface, (0, 0))

		if self._viewmsg:
			self._screen.blit(self._message_surf, (0,0))

		pygame.display.flip()

	def _aspect_scale(self,img,(bx,by)):
		""" Scales 'img' to fit into box bx/by.
		 This method will retain the original image's aspect ratio """
		ix,iy = img.get_size()
		if ix > iy:
			# fit to width
			scale_factor = bx/float(ix)
			sy = scale_factor * iy
			if sy > by:
				scale_factor = by/float(iy)
				sx = scale_factor * ix
				sy = by
			else:
				sx = bx
		else:
			# fit to height
			scale_factor = by/float(iy)
			sx = scale_factor * ix
			if sx > bx:
				scale_factor = bx/float(ix)
				sx = bx
				sy = scale_factor * iy
			else:
				sy = by

		return pygame.transform.scale(img, (int(sx),int(sy)))

	def idle(self):
		self._main_surface.blit(self._idle_surface, (0,0))
		self._draw()

	def update(self, name=None, drinks=None, total=0, bill=(0,0)):
		self._main_surface = self._main_bg.copy()

		if name:
			name_surf = self._font.render(name, True, self._text_fg_color)
			name_surf = self._aspect_scale(name_surf, (self._x_unit*8, self._y_unit*2))
			try:
				avatar_surf = pygame.image.load(get_avatar(name))
			except:
				try:
					avatar_surf = pygame.image.load(NOAVATAR_PATH)
				except:
					self.logger.critical("Could not load default avatar")
					sys.exit()

			avatar_surf.convert()
			avatar_surf = self._aspect_scale(avatar_surf, (self._x_unit*1.9, self._x_unit*1.9))

			self._main_surface.blit(avatar_surf, (0,0))
			self._main_surface.blit(name_surf, (self._x_unit*2, 0))

		if drinks:
			drink_height = (12*self._y_unit)/8

			for i, drink in enumerate(drinks[:-9:-1]):
				if len(drinks)>8 and i==7:
					drink_surf = self._font.render("und noch %s mehr" % (len(drinks)-7), True, self._text_bg_color)
					price_surf = self._font.render("...", True, self._text_bg_color)
				else:
					if i==0:
						drink_surf = self._font.render(drink[0], True, self._text_fg_color)
						price_surf = self._font.render("%.2f" % drink[1], True, self._text_fg_color)

						try:
							drink_img_surf = pygame.image.load(get_drink(drink[0]))
						except:
							try:
								drink_img_surf = pygame.image.load(NODRINK_PATH)
							except:
								self.logger.critical("Could not load default image")
								sys.exit()
					else:
						drink_surf = self._font.render(drink[0], True, self._text_bg_color)
						price_surf = self._font.render("%.2f" % drink[1], True, self._text_bg_color)

				drink_surf = self._aspect_scale(drink_surf, (5*self._x_unit*0.95, drink_height))
				price_surf = self._aspect_scale(price_surf, (2*self._x_unit*0.95, drink_height))

				self._main_surface.blit(drink_surf, (8*self._x_unit-drink_surf.get_width() - self._x_unit*0.1, (7*(self._res_y/8))-((i+1)*drink_height)))
				self._main_surface.blit(price_surf, (self._res_x-price_surf.get_width(), (7*(self._res_y/8))-((i+1)*drink_height)))

			drink_img_surf = self._aspect_scale(drink_img_surf, (self._x_unit*1.9, self._x_unit*1.9))
			self._main_surface.blit(drink_img_surf, (self._x_unit*0.2, 14*self._y_unit*0.95 - drink_img_surf.get_height()))

		total_surf = self._font.render("Summe:", True, self._text_fg_color)
		total_surf = self._aspect_scale(total_surf, (3*self._x_unit, 2*self._y_unit))
		self._main_surface.blit(total_surf, ((8*self._x_unit-total_surf.get_width()) , 14*self._y_unit))

		total_surf = self._font.render("%.2f" % total, True, self._text_fg_color)
		total_surf = self._aspect_scale(total_surf, (2*self._x_unit, 2*self._y_unit))
		self._main_surface.blit(total_surf, ((self._res_x-total_surf.get_width()) , 14*self._y_unit))

		bill_surf = self._font.render("Laufende Rechnung: %.2f" % bill[0], True, self._text_fg_color)
		bill_surf = self._aspect_scale(bill_surf, (4*self._x_unit, 1*self._y_unit))
		self._main_surface.blit(bill_surf, (0.1*self._x_unit, 14*self._y_unit))
		bill_surf = self._font.render("Offene Rechnungen: %.2f" % bill[1], True, self._text_fg_color)
		bill_surf = self._aspect_scale(bill_surf, (4*self._x_unit, 1*self._y_unit))
		self._main_surface.blit(bill_surf, (0.1*self._x_unit , 15*self._y_unit))

		self._draw()

	def message(self, text, heading=None , delay=DEFAULT_MESSAGE_DELAY, align=DEFAULT_MESSAGE_ALIGN):
		self.message_on(text=text, heading=heading, align=align)
		self.message_off(delay=delay)

	def message_on(self, text, heading=None, align=DEFAULT_MESSAGE_ALIGN, delay=None):
		self._message_surf = self._message_bg.copy()

		try:
			self._message_surf.blit(render_textrect( \
				heading, self._message_head_font, pygame.Rect((0,0),(6*self._x_unit, 2*self._y_unit)), \
				self._text_fg_color, pygame.Color('#00000000'), 1 \
				), (2*self._x_unit, 4*self._y_unit))

			self._message_surf.blit(render_textrect( \
				text, self._message_font, pygame.Rect((0,0),(6*self._x_unit, 6*self._y_unit)), \
				self._text_fg_color, pygame.Color('#00000000'), 1 \
				), (2*self._x_unit, 6*self._y_unit))
		except:
			self.logger.error("Message text too long")

		self._viewmsg = True
		self._draw()

	def message_off(self, delay=None):
		if delay and delay > 0:
			time.sleep(delay)
		self._viewmsg = False
		self._draw()