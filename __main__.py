#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from handler import auto_update, scanner
from display import *


def main(*cmd_args):
	#display_empty()
	lcd = Display()

	lcd.idle()
	lcd.message("ERROR: Wrong code!")
	lcd.update(name = "Penis Ulrich")
	#lcd.update(drinks = [(u"Sääääääääääääääääft", 1.56),("Bowasser", 2.3)], total = 13.37)
	lcd.update(drinks = [("foo",12.33),("Jizz", 34.00),(u"Säft", 1.56),("Bier", 4.5),("Bowasser", 2.3)], total = 13.37)
	lcd.message("OH HAI!")
	#lcd.idle()
	#lcd.update(name = "Horst")

	auto_update()
	scanner()


if __name__ == '__main__':
	main(*sys.argv[1:])