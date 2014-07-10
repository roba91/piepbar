#!/usr/bin/env python
# -*- coding: utf-8 -*-

from displaydriver import DisplayDriver
from PIL import Image
import cProfile
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

dc = DisplayDriver("/dev/pidisplay",76800)
im = Image.open("data/idle_bg.png")
dc.send_image(im)
#cProfile.run("dc.send_image(im)")


