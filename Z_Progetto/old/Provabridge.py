#!/usr/bin/python3
import os
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import Intf
from mininet.log import setLogLevel, info

def myNetwork():

	net = Mininet( topo=None, build=False)

	info( '*** Adding controller\n' )
	net.addController(name='c0')

	info( '*** Add switches\n')
	s1 = net.addSwitch('s1')
	Intf( 'eth1', node=s1 )
	s1.cmd('ovs-vsctl add-port s1 eth1')
	#s1.cmd('ifconfig s1 192.168.33.30') #not works
	

	info( '*** Add hosts\n')
	h1 = net.addHost('h1', ip='192.168.33.31/24')
	h2 = net.addHost('h2', ip='192.168.33.32/24')

	info( '*** Add links\n')
	net.addLink(h1, s1)
	net.addLink(h2, s1)

	info( '*** Starting network\n')
	net.start()
	os.system("ifconfig s1 192.168.33.30")
	#h1.cmdPrint('dhclient -4 '+h1.defaultIntf().name)
	CLI(net)
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	myNetwork()
