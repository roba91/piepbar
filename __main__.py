#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging

from handler import auto_update, scanner
from color_display import *
from handler.config import *


def main(*cmd_args):
	#lcd = Display()

	#lcd.message("ERROR: Wrong code!")
	#lcd.update(name = "Penis Ulrich")
	#lcd.update(drinks = [(u"Sääääääääääääääääft", 1.56),("Bowasser", 2.3)], total = 13.37)
	# lcd.update(drinks = [("foo",12.33),("Jizz", 34.00),(u"Säft", 1.56),("Bier", 4.5),("Bowasser", 2.3)], total = 13.37)
	# lcd.message("I didn't know\nit was you", heading="OH HAI MARC!")
	# lcd.message("Thanks,\nyou're my favourite\ncostumer!", align='center')
	#lcd.idle()
	#lcd.update(name = "Horst")


	logging.basicConfig(filename=LOG_FILE,level=LOG_LEVEL, format=LOG_FORMAT, datefmt=LOG_DATEFORMAT)
	logger = logger = logging.getLogger("main")
	
	logger.info("System started")
	auto_update()
	scanner()
	logger.info("System shutting down")

if __name__ == '__main__':
	main(*sys.argv[1:])