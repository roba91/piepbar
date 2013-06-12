#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
#from handler import handle_scanning as scan
from display import *

def init():
	display_init()

def main(*cmd_args):
	scan()
	init()

if __name__ == '__main__':
	main(*sys.argv[1:])