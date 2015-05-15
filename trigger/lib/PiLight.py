# Library to generate and manipulate data from a pilight-daemon socket
# Author : Sarrailh Remi
# Copyright: Gplv3
#
# based on pilight clients example
# https://github.com/pilight/pilight/blob/master/clients/process.py
# Author: CurlyMo
# Copyright: Gplv3

import time
import socket
import struct
import json
import re
import csv
import sys
import os

#Search for pilight socket
def discover(service, timeout=2, retries=1):
	group = ("239.255.255.250", 1900)
	message = "\r\n".join([
		'M-SEARCH * HTTP/1.1',
		'HOST: {0}:{1}'.format(*group),
		'MAN: "ssdp:discover"',
		'ST: {st}','MX: 3','',''])


	responses = {}
	i = 0;
	for _ in range(retries):
		i += 1
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, struct.pack('LL', 0, 10000));
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		sock.sendto(message.format(st=service), group)
		while True:
			try:
				responses[i] = sock.recv(1024);
				break;
			except socket.timeout:
				sys.stdout.write("pilight-daemon : Timeout\n")
				sys.exit(1)
				break;
			except:
				sys.stdout.write("pilight-daemon : Not Founded\n")
				os.system("service pilight restart")
				sys.exit(2)
				break;
		return responses.values()

#Get location and port 
def getInfo():
	responses = discover("urn:schemas-upnp-org:service:pilight:1");
	if len(responses) > 0:
		locationsrc = re.search('Location:([0-9.]+):(.*)', str(responses[0]), re.IGNORECASE)
		if locationsrc:
			location = locationsrc.group(1)
			port = locationsrc.group(2)
			print location + ":" + str(port)
			return (location,port)

#Connect and identify
def connect():
	location, port = getInfo()
	#Generate socket	
	pilightSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket.setdefaulttimeout(0)
	pilightSocket.connect((location, int(port)))

	#Send client identification
	pilightSocket.send('{"action":"identify","options":{"receiver":1}}\n')
	return pilightSocket

#Check if string is valid json
#http://stackoverflow.com/questions/5508509/how-do-i-check-if-a-string-is-valid-json-in-python
def is_json(jsonData):
	try:
		json_object = json.loads(jsonData)
	except ValueError, e:
		return False
	return True

#Check buffer and extract radio code only
def getRadioCode(buffer):
	radiocode = False

	#We split the buffer into multiples lines
	for line in iter(buffer.splitlines()):
		#If the line is json
		if is_json(line):
			parsed_json = json.loads(line)
			#If json is about a radio message
			if (
				parsed_json.get('message') and 
				parsed_json.get('protocol') and
				parsed_json.get('repeats')
				):
				
				#We extract useful information
				protocol = parsed_json["protocol"]
				message = parsed_json["message"]
				repeats = parsed_json["repeats"]

				#Transform json into a compact form
				radiocode = protocol
				for item in message:
					radiocode = radiocode + ";" + str(message[item])
	return radiocode