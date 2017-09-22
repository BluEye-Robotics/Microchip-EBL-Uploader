#!/usr/bin/env python

__author__ = "Johannes Schrimpf"
__copyright__ = "Copyright (C) 2017 Blueye Robotics AS"
__license__ = "GPL3"
__version__ = "0.1"

import serial
import struct
import sys

if len(sys.argv) < 2:
    exit()
fn = sys.argv[1]

with open(fn, mode='rb') as fh:
    fw = fh.read()

ser = serial.Serial('/dev/ttyUSB0', 115200)

chunk_len = 64
while len(fw) > 0:
    ser.write(fw[:chunk_len])
    fw = fw[chunk_len:]
    data = ser.read(2)
    chunk_len = struct.unpack("=h", data)[0]
    while chunk_len < 0:
        data = ser.read(2)
        chunk_len = struct.unpack("=h", data)[0]
        print "Wating for bootloader to request data"
    print "Chunk_len:", chunk_len, "Remaining:", len(fw)

ser.close()
