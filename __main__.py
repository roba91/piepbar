#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from handler import auto_update, scanner
#import display # TODO: remove - just for testing the init of this module

def main(*cmd_args):
	auto_update()
	scanner()

if __name__ == '__main__':
	main(*sys.argv[1:])