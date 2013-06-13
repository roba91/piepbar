#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
from time import sleep
from crcmod.predefined import mkCrcFun

class DisplayDriver(object):
	
	def __init__(self, port="/dev/pidisplay", baudrate=76800, dummy=False):
		self._dummy = dummy
		
		if not dummy :
			self._ser = serial.Serial(port, baudrate, timeout=0.100)
			if not self._ser:
				raise ValueError("Unable to open %s with %d baud" % (port, baudrate))

			self._crc16 = mkCrcFun('crc16')

	def _build_packet(self, data):
		crc = self._crc16(data)
		return data + chr((crc & 0xFF00) >> 8) + chr(crc & 0x00FF) 


	def _send_half_image(self, data, half):
		success = False
		paket = self._build_packet(data)
		req = chr(0xD0 | half)
		resp = chr(0xA0 | half)
		ack = chr(0xAA)
		if half == 1 :
			ack = chr(0xAB)

		while not success:
			self._ser.write(req)
			while not self._ser.read() == resp:
				self._ser.write(req)

			print "[DisplayDriver] Request was acked"

			self._ser.write(paket)

			byte = self._ser.read()
			retries = 0
			while byte != ack and retries < 5:
				byte = self._ser.read()
				retries = retries + 1

			success = (byte == ack)

		print "[DisplayDriver] Data was acked"


	def _pixel_to_byte(self,pixels,x,y):
		byte = 0
		for i in range(8):
			byte =  byte | ((pixels[x+i,y] == 0) << i) 
		return byte

	def send_image(self, image):
		if self._dummy :
			image.show()
			return


		pixels = image.load()

		data = ""

		w,h = image.size
		for y in range(h):
			for x in range(0,w,8):
				data = data + chr(self._pixel_to_byte(pixels,x,y))

		self._send_half_image(data[:800],0)
		self._send_half_image(data[800:],1)