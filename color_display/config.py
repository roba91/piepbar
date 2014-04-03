#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join, dirname
# TODO: move more hard-coded option and default values to this place -> please Freddi, be more pythonic :)


############################## display settings ###############################
def get_data_path(file_name):
	return join(dirname(__file__), 'data', file_name)

MOVIE = get_data_path('oos.mpg')

IDLE_PATH = get_data_path('idle_bg.png')
MAIN_PATH = get_data_path('main_bg.png')

FONT_PATH = get_data_path('Terminus.ttf')
BOLD_PATH = get_data_path('TerminusBold.ttf')
DITHER_PATH = get_data_path('dither_mask.png')

DUMMY_DISPLAY = True # Set to false to use the real hardware


############################## message settings ###############################
DEFAULT_MESSAGE_DELAY = 3
DEFAULT_MESSAGE_ALIGN = 'center'
