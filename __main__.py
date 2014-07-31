#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging

from handler import auto_update, handle_input
from handler.config import *

from gui import Gui

import pygame
from pygame.locals import *

screen = None

def init():
	pygame.init()
	pygame.font.init()
	global screen
	screen = pygame.display.set_mode((480,272)) # Set fullscreen here
	pygame.mouse.set_visible(False)

def event_loop(gui):
	input_string = ''

	gui.idle()
	#gui.update(total=12.66, name="f_walk09", bill=(4.33, 123.44), drinks = [("Wasser",1.33),("Wasser",1.33),("Wasser",1.33),("Wasser",1.33),("Flensburger", 3.00),(u"Schöfferhofer Grapefruit", 1.56),("Orangina", 4.5),("Kaffee", 2.3), ("Club-Mate", 1.00)])

	while True:
		pygame.time.wait(1)
		for event in pygame.event.get(): # User did something
			if event.type == KEYDOWN:
				gui.unidle()

				if event.key == pygame.K_RETURN:
					print 'Handling: %s' % input_string
					handle_input(input_string, gui)
					input_string = ''
				else:
					input_string += event.unicode

		if event.type == pygame.QUIT: # If user clicked close
				print "\n>>> Fools, don't let them escape! <<<\n"
				pygame.quit()
				sys.exit(0) # for testing reasons

def main(*cmd_args):
	#display_empty()
	# lcd = Display()

	#lcd.idle()
	#lcd.message("ERROR: Wrong code!")
	# lcd.update(name = "Penis Ulrich")
	#lcd.update(drinks = [(u"Sääääääääääääääääft", 1.56),("Bowasser", 2.3)], total = 13.37)
	# lcd.update(drinks = [("foo",12.33),("Jizz", 34.00),(u"Säft", 1.56),("Bier", 4.5),("Bowasser", 2.3)], total = 13.37)
	# lcd.message("I didn't know\nit was you", heading="OH HAI MARC!")
	# lcd.message("Thanks,\nyou're my favourite\ncostumer!", align='center')
	#lcd.idle()
	#lcd.update(name = "Horst")

	logging.basicConfig(filename=LOG_FILE,level=LOG_LEVEL, format=LOG_FORMAT, datefmt=LOG_DATEFORMAT)
	logger = logger = logging.getLogger("main")

	init()

	logger.info("System started")
	auto_update()
	event_loop(Gui(screen))
	logger.info("System shutting down")

if __name__ == '__main__':
	main(*sys.argv[1:])