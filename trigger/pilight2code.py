#!/usr/bin/env python
#
# pilight2triggers
# Control your pi from an arduino / radio remote easily
# Use Pilight to receive radio code and execute commands based on them
# 
# Author : Sarrailh Remi
# Copyright : Gplv3
#
# based on pilight clients example
# https://github.com/pilight/pilight/blob/master/clients/process.py
# Author: CurlyMo
# Copyright: Gplv3

import socket
import sys
from lib import PiLight

#Connect to pilight-daemon
sys.stdout.write("Collector: pilight-daemon\n")
pilightSocket = PiLight.connect();


sys.stdout.write("--------------------------\n")
sys.stdout.write("waiting for code...\n")
sys.stdout.write("To exit press [Ctrl-C]\n")

try:
    while True:
        #We read the buffer
        buffer = pilightSocket.recv(1024)
        #Check if a radiocode exists and format it in a small format
        radiocode = PiLight.getRadioCode(buffer)
        if radiocode != False:
            print radiocode          
except KeyboardInterrupt:
    sys.stdout.write("-----------------------\n")
    sys.stdout.write("Radio Sniffer OFF\n")
    pilightSocket.close()
