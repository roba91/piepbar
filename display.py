#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
from crcmod.predefined import mkCrcFun

class DisplayConnection(object):
	

	def __init__(self, port, baudrate=115200):
		self._ser = serial.Serial(port, baudrate, timeout=0.5)
		self._crc16 = mkCrcFun('crc16')

	def _build_packet(self, data):
		crc = self._crc16(data)
		return data + chr((crc & 0xFF00) >> 8) + chr(crc & 0x00FF) 

	def _send_half_image(self, data, half):
		success = False
		print data
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

			self._ser.write(paket)
			success = (self._ser.read() == ack)
