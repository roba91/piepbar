#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join, dirname
from os import listdir
import random
# TODO: move more hard-coded option and default values to this place -> please Freddi, be more pythonic :)


############################## display settings ###############################
def get_data_path(file_name):
	return join(dirname(__file__), 'data', file_name)

def get_avatar(user):
	return join(dirname(__file__), 'data/avatars', user+'.png')

def get_drink(name):
	return join(dirname(__file__), 'data/drinks', name+'.png')

def get_random_movie():
	files = [k for k in listdir(join(dirname(__file__), 'data/movies')) if k.endswith('.mpg')]
	return join(dirname(__file__), 'data/movies', random.choice(files))

IDLE_PATH = get_data_path('idle_bg.png')
MAIN_PATH = get_data_path('main_bg.png')
MESSAGE_PATH = get_data_path('message.png')
NOAVATAR_PATH = get_avatar('default')
NODRINK_PATH = get_drink('default')


''' Reencode videos with: ffmpeg -i <infile> -vf scale=480:272 -vcodec mpeg1video -acodec libmp3lame -intra <outfile.mpg>'''
IDLE_VIDEO_TIMEOUT = 30

FONT_PATH = get_data_path('RopaSans-Regular.ttf')
BOLD_PATH = get_data_path('TerminusBold.ttf')
DITHER_PATH = get_data_path('dither_mask.png')

DEFAULT_MESSAGE_DELAY = 3
DEFAULT_MESSAGE_ALIGN = 'center'