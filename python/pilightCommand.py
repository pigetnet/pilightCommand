#!/usr/bin/env python
#
# pilightCommand
# Control your pi from an arduino / radio remote easily
# Use Pilight to receive radio code and execute commands based on them
#
# Author : Sarrailh Remi
# Copyright : Gplv3
#
# based on pilight client example
# https://github.com/pilight/pilight/blob/master/clients/process.py
# Author: CurlyMo
# Copyright: Gplv3

import socket
import sys
from lib import Commands
from lib import PiLight
from lib import TriggersINI

# Commands.send("printenv")
configurationFile = "/opt/user/config/pilight/pilightCommand.cfg"
sys.stdout.write("Radio Triggers ON\n")

# Get triggers from configuration file
triggers = TriggersINI.openConfiguration(configurationFile)
if triggers is not False:
    sys.stdout.write("Configuration: " + configurationFile + "\n")
else:
    sys.stdout.write("Configuration: " + configurationFile + " failed to load\n")
    sys.exit(1)

# Connect to pilight-daemon
pilightSocket = PiLight.connect()

sys.stdout.write("Collector: pilight-daemon\n")
sys.stdout.write("--------------------------\n")
sys.stdout.write("waiting for code...\n")
sys.stdout.write("To exit press [Ctrl-C]\n")

try:
    while True:
        # We read the buffer
        buffer = pilightSocket.recv(1024)
        # Check if a radiocode exists and format it in a small format
        radiocode = PiLight.getRadioCode(buffer)
        if radiocode is not False:
            sys.stdout.write("CODE: "+radiocode+"\n")

        action = TriggersINI.checkTrigger(triggers, radiocode)

        if action is not False:
            sys.stdout.write("\n")
            sys.stdout.write("COMMAND: "+action+"\n")
            sys.stdout.write("-------------\n")
            Commands.send(action)
except KeyboardInterrupt:
    sys.stdout.write("-----------------------\n")
    sys.stdout.write("Radio Triggers OFF\n")
    pilightSocket.close()
