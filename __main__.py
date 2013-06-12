#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from handler import handle_scanning as scan

def main(*cmd_args):
	scan()

if __name__ == '__main__':
	main(*sys.argv[1:])