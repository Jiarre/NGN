Disable and Stop systemd-resolved.service in commnetsemu for free update of /etc/resolv.conf

sudo systemctl stop systemd-resolved.service
sudo rm /etc/resolve.conf (it's a symlink) 

## How to run the project ##
- Connect dhcp/dns to comnetsemu's eth1
- ryu-manager ryu_controller.py
- sudo python3 network.py [-s][-h]
- Execute backgroundDNSServer on dhcp/dns server

## How to wakeup / shutdown hosts ##
On a mininet's child node execute "sendPacketHost.py" and specify mac-address or hostname
if the backgroundDNSServer is running hostname and mac specified will wake up, else nothing will happen

## How to get information ##
Even if you can't ping down hosts you can still use "getStatusHost" to get the status of every host of the network


## Limitations ##
Maximum number of hosts is 255
