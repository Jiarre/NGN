#!/usr/bin/python3
import controllerHost
from datetime import datetime


print("--- Listening ---")
print(str(datetime.now()) + '\n', flush=True)
while True:
	controllerHost.get_request_to_dnsserver()
	print("Destination host recieved, forward the creation of personal packet")
	controllerHost.send_packet(None)
	print(str(datetime.now()) + '\n', flush=True)
