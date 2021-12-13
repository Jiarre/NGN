## How to run the project ##
- Connect dhcp/dns to comnetsemu's eth1
- ryu-manager ryu_controller.py
- sudo python3 network.py [-s][-h][-dhcp]
- Execute backgroundDNSServer.py on dhcp/dns server

All the executions fo commands in mininet (and hosts xterm) must run without 'sudo' prefix

## How to wakeup / shutdown hosts ##
On a mininet's child node execute "sendPacketHost.py" and specify mac-address or hostname
if the backgroundDNSServer is running hostname and mac specified will wake up, else nothing will happen

## How to get information ##
Even if you can't ping down hosts you can still use "getStatusHost.py" to get the status of every host of the network

With "getLogHost.py" you can see the history on activities of the provided host


## Limitations ##
Maximum number of hosts is:
- 99 (with dhcp)
- 255 (within mininet)

Minimum number of switches is 1


If manually stop mininet script when DHCP requests of hosts are running,
restore machine hostname with "sudo hostname HOSTNAME"