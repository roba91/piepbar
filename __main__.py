#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from handler import auto_update, scanner
from display import *


def main(*cmd_args):
	display_empty()
	display_name("Penis Ulrich")
	display_products([("Jizz", 34.00),("Säft", 1.56),("Bier", 4.5),("Bowasser", 2.3)],13.37)
	display_draw()
	auto_update()
	scanner()


if __name__ == '__main__':
	main(*sys.argv[1:])