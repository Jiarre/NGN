#!/usr/bin/python3
import controllerHost
import sys

host = sys.argv[1]
status = controllerHost.get_status(host)
print(f"{host} is currently {status}")
controllerHost.ipt_roules(status)
while True:
	controllerHost.get_packet()
