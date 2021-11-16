#!/usr/bin/python3
import controllerHost
import sys
import os
from datetime import datetime

host = sys.argv[1]
print(datetime.now())
print("b")
#print(os.system("export"))
status = controllerHost.get_status(host)
print(f"{host} is currently {status}")
controllerHost.ipt_roules(status)
print("---Listening---")
while True:
	controllerHost.get_packet()
	print(str(datetime.now()) + '\n')
