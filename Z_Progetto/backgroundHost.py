#!/usr/bin/python3
import controllerHost
import sys
import os
from datetime import datetime

host = sys.argv[1]
if len(sys.argv) > 2:
	fout = os.open(sys.argv[2], os.O_CREAT | os.O_WRONLY, 0o777)
	sys.stdout = open(fout, 'a')
print(datetime.now())
status = controllerHost.get_status(host)
print(f"{host} is currently {status}")
controllerHost.ipt_roules(status)
print("---Listening---")
while True:
	controllerHost.get_packet()
	print(str(datetime.now()) + '\n')
	if len(sys.argv) > 2:
		sys.stdout.close()
		sys.stdout = open(fout, 'a')
