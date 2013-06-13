#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gnulpf import gnulpf_str
from displaydriver import DisplayDriver
from PIL import Image
import cProfile

dc = DisplayDriver("/dev/pidisplay",76800)
im = Image.open("test.png")
cProfile.run("dc.send_image(im)")


