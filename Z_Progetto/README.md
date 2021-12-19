## How to run the project ##
- Connect dhcp/dns to comnetsemu's eth1
- ryu-manager ryu_controller.py
- sudo python3 network.py [-s][-h][-dhcp]
- Execute backgroundDNSServer.py on dhcp/dns server

All the executions for commands in mininet (and hosts xterm) must be run without 'sudo' prefix

## How to wakeup / shutdown hosts ##
On a mininet's child node execute "sendPacketHost.py" and specify mac-address or hostname
if the backgroundDNSServer is running hostname and mac specified will wake up, if not only specified macs will wake up

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

## Known Problems ##
On a fresh comnetsemu machine, the first time you try executing any ryu script it'll throw "Already Handled" exception. In this case you'll just need to run "pip install eventlet==0.30.2" and restart the ryu script. If you are stuck with the DNS configuration from the project and can't reach internet just edit (or create) the file /etc/resolv.conf and as the first line "nameserver 8.8.8.8"

Rarely the error "Unsupported version 0x1" could pop up in ryu console. Just stop ryu and mininet and perform a mininet clear with "sudo mn -c"
