#!/usr/bin/python3
import os

sdir = "/tmp/NGN/hosts"
files = sorted(os.listdir(sdir), key=lambda x: (len(x), x))
for f in files:
	file = open(sdir + "/" + f, 'r')
	print(f"{f} is {file.read()}")
	file.close()
