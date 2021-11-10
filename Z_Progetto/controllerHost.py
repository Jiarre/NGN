#!/usr/bin/python3
import os
import subprocess
import socket
import re

"""
creare pacchetto eth personale (solo mac dest)
paccheto WOL lo fa ryu sul controller
parser di controllo sul pacchetto eth personale
	-> cancellazione regola ip table in base la valore all'interno di un file
"""


def ipt_roules(status):

	# Get local ip
	ip = subprocess.check_output("hostname -I | awk '{print $1}'", shell=True).decode("utf-8")[:-1]

	if status == "DOWN":
		# Add Rule
		os.system("iptables -A INPUT -d "+ip+" -j REJECT")
	else:
		# Delete Rule
		os.system("iptables -D INPUT -d "+ip+" -j REJECT")


def create_packet(mac_src):
	eth_type = bytes.fromhex("1111")  # int -> 4369
	mac_dst = bytes.fromhex("F"*12)

	wol_dst = input("Provide the hostname or complete MAC address\n"
									"(accepted separator separator [:-\s]) of the machine to WOL: ")
	# Check mac address format
	addr = re.fullmatch(
		'^([A-F0-9]{2}(([:][A-F0-9]{2}){5}|([-][A-F0-9]{2}){5})|([s][A-F0-9]{2}){5})|'
		'([a-f0-9]{2}(([:][a-f0-9]{2}){5}|([-][a-f0-9]{2}){5}|([s][a-f0-9]{2}){5}))$',
		wol_dst)
	hostname = re.fullmatch('^h[0-9]*',	wol_dst)

	# 1 match, or the MAC is invalid
	if addr:
		# Remove mac separator [:-\s] and convert to bytes
		mac_addr = bytes.fromhex(wol_dst.replace(wol_dst[2], ''))
	else:
		if hostname:
			# Get index of the host and create MAC address from that with padding
			mac_addr = bytes([int(wol_dst.replace('h', ''))]).rjust(6, b'\x00')
		else:
			raise ValueError('Incorrect MAC address format or hostname')

	# The message is compose by the mac address of machine that would receive the WOL Magic Packet
	data = mac_addr
	payload = mac_dst + mac_src + eth_type + data

	return payload


def send_packet():

	s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
	if len(socket.if_nameindex()) > 2:
		for x in socket.if_nameindex():
			print(str(x[0]) + " -> " + x[1])
		idx = input("Choose the index of the interface where send the packet: ")
	else:
		# Speed up in best case scenarios, excluding loopback interface
		idx = 2

	interface = socket.if_indextoname(idx)
	# Specification seams not working, only interfeace is necessary
	s.bind((interface, 0x1111, socket.PACKET_BROADCAST))
	data = create_packet(s.getsockname()[4])
	s.send(data)


def get_packet():
	#
	return


def check_packet():
	#
	return


# MAIN


send_packet()
