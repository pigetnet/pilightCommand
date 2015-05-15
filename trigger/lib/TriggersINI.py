#!/usr/bin/python
# This libraries execute actions based on string it receives
# It searches for a configuration files where all actions is format as a ini files
#
# Author : Sarrailh Remi
# Copyright : Gplv3

import sys
import time
import os
import ConfigParser
from subprocess import call

#We only open the configuration at the beginning
#Every modification will be made only on memory (for locking actions)
def openConfiguration(configurationFile):
	#Check configuration files
	fileExists = os.path.isfile(configurationFile)
	
	if(fileExists):
		#Read the configuration files
		settings = ConfigParser.ConfigParser()
		settings.read(configurationFile)	
		
		configurationChecked = CheckConfiguration(settings)
		if configurationChecked:
			return settings
		else:
			return False
	else:
		sys.stdout.write(configurationFile + " doesn't exists!\n")
		return False
	return False


def CheckConfiguration(settings):
	sections = settings.sections();
	for section in sections:
		if (
			settings.has_option(section,'action') and
			settings.has_option(section,'timer')
			):
			sys.stdout.write("CODE: " + section + "\n")
		else:
			sys.stdout.write("CODE: " + section + " -- Failed\n")
			return False
	return True

#Check trigger (code exists ? is action lock?)
def checkTrigger(triggers,codeToCheck):
	if codeToCheck != False:
		
		#Each sections is a code
		codesTriggers = triggers.sections();

		#Check if code exists
		codeExists = checkCode(codesTriggers,codeToCheck)
		
		#If codes exists check lock
		if codeExists:
			lock = checkLock(triggers,codeToCheck)
			if lock == False:
				return triggers.get(codeToCheck,"action")
		else:
			return False
	
	return False


#Check if a code exists inside the configuration file
def checkCode(codesTriggers,codeToCheck):
	for code in codesTriggers:
		if (code == codeToCheck):
			return True
	return False

#Check if a lock exists for the code in the configuration file
def checkLock(triggers,code):
	if triggers.has_option(code,'lock'):
		time_start = time.time()
		time_stop = triggers.get(code,'lock',True)
					
		#if the timer has ended
		if time_start > time_stop:
			#triggers.remove_option(code,'lock')
			lockUntilTime = time.time() + triggers.getint(code,'timer')
			triggers.set(code,'lock',lockUntilTime)
			#sys.stdout.write("Action : OK (timer ended)")
			return False
		else:
			#sys.stdout.write("Action : Locked by timer")
			return True
	else:
		#Save timestamp
		#sys.stdout.write("Action : OK")
		lockUntilTime = time.time() + triggers.getint(code,'timer')
		triggers.set(code,'lock',lockUntilTime)
		return False