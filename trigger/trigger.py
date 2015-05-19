#!/usr/bin/python
# This programs is the link between
# rfreceive (the trigger) and the actions directory
# By Sarrailh Remi

import sys
import time
import os
import ConfigParser
from subprocess import call

configurationFile = "/boot/piget/config/pilightCommand.cfg"

#Read the configuration files
settings = ConfigParser.ConfigParser()
settings.read(configurationFile)

#Each sections is a codes
list_codes = settings.sections()

#Launch Triggers
def launch_triggers( arg ):
	for code in list_codes:
		#print arg
		#If a code in actions.cfg match the code received
		if (code == arg ):
				#Verify if the timer has ended
				if settings.has_option(code,'lock'):
					time_start = time.time()
					time_stop = settings.getfloat(code,'lock')
					
					#if the timer has ended
					if time_start > time_stop:
						settings.remove_option(code,'lock')
						settings.write(open(configurationFile,'w'))
					else:
						#os.system("./actions/led 3")
						print "Action is locked"
				else:
					#Save timestamp
					settings.set(code,'lock',time.time() + settings.getint(code,'timer'))
					settings.write(open(configurationFile,'w'))

					#Launch actions
					action = settings.get(code,"action")
					print arg
					print "Launching: " + action
					os.system(action)
#Main Functions
if len(sys.argv) == 2:
	launch_triggers(sys.argv[1])
else:
	print "Wrong Number of Arguments"
