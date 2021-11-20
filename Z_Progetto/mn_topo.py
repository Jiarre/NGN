import os
import shutil
import sys
import time

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, OVSSwitch
from mininet.term import makeTerm

SDIR = "/tmp/NGN/hosts"
TONULL = "&>/dev/null"
DHCP = False
if len(sys.argv) > 1:
    if sys.argv[1] == '-dhcp':
        DHCP = True

class MinimalTopo( Topo ):

    def build( self ):
        hosts = []
        h1 = self.addHost('h1', ip=None)
        h2 = self.addHost('h2', ip=None)
        h3 = self.addHost('h3', ip=None)
        h4 = self.addHost('h4', ip=None)
        h5 = self.addHost('h5', ip=None)
        h6 = self.addHost('h6', ip=None)
        h7 = self.addHost('h7', ip=None)
        h8 = self.addHost('h8', ip=None)
        h9 = self.addHost('h9', ip=None)
        h10 = self.addHost('h10', ip=None)
        h11 = self.addHost('h11', ip=None)
        h12 = self.addHost('h12', ip=None)

        hosts.append(h1)
        hosts.append(h2)
        hosts.append(h3)
        hosts.append(h4)
        hosts.append(h5)
        hosts.append(h6)
        hosts.append(h7)
        hosts.append(h8)
        hosts.append(h9)
        hosts.append(h10)
        hosts.append(h11)
        hosts.append(h12)


        # Create switches
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )
        s3 = self.addSwitch( 's3' )
        s4 = self.addSwitch( 's4' )


        # Add links between the switch and each host
        self.addLink( s1, h1 )
        self.addLink( s1, h2 )
        self.addLink( s1, h3 )

        self.addLink( s2, h4 )
        self.addLink( s2, h5 )
        self.addLink( s2, h6 )

        self.addLink( s3, h7 )
        self.addLink( s3, h8 )
        self.addLink( s3, h9 )

        self.addLink( s4, h10 )
        self.addLink( s4, h11 )
        self.addLink( s4, h12 )

        self.addLink( s1, s2 )
        self.addLink( s3, s4 )
        self.addLink( s3, s2 )

        print("*** Setting files and directories")
        os.umask(0000)
        if os.path.exists(SDIR):
            shutil.rmtree(SDIR)
        os.makedirs(f"{SDIR}/LOGs")
        os.environ["statusdir"] = SDIR

        for h in hosts:
            host = str(h)
            fileS = f"{SDIR}/{host}"
            fileL = f"{SDIR}/LOGs/{host}.log"
            # Set status file
            try:
                os.close(os.open(fileL, os.O_CREAT | os.O_WRONLY, 0o777))
                f = open(os.open(fileS, os.O_CREAT | os.O_WRONLY, 0o777), 'w')
                if host == "h1":
                    # Only h1 stars UP
                    f.write("UP")
                else:
                    f.write("DOWN")
                f.close()
            except OSError:
                print("Failed creating files")
            else:
                print(f"Files of host {host} created")


def runMinimalTopo():
    # Create an instance of our topology
    topo = MinimalTopo()

    # Create a network based on the topology using OVS and controlled by
    # a remote controller.
    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController( name, ip='127.0.0.1' ),
        switch=OVSSwitch,
        autoSetMacs=True )

    # Actually start the network
    net.start()
    # Drop the user in to a CLI so user can run commands.
    node1 = net.getNodeByName("s1")
    node2 = net.getNodeByName("s2")
    node3 = net.getNodeByName("s3")
    node4 = net.getNodeByName("s4")
    print("*** Setting basic flow on switches")
    node1.cmd("sudo ovs-ofctl add-flow s1 dl_type=0x1111,action=controller")
    node2.cmd("sudo ovs-ofctl add-flow s2 dl_type=0x1111,action=controller")
    node3.cmd("sudo ovs-ofctl add-flow s3 dl_type=0x1111,action=controller")
    node4.cmd("sudo ovs-ofctl add-flow s4 dl_type=0x1111,action=controller")

    print("*** Setting up bridge network")
    node1.cmd('sudo ovs-vsctl add-port s1 eth1')

    if not DHCP:
        print("*** Setting up static IP")
        net.getNodeByName("h1").setIP(ip="192.168.1.11", prefixLen=24)
        net.getNodeByName("h2").setIP(ip="192.168.1.12", prefixLen=24)
        net.getNodeByName("h3").setIP(ip="192.168.1.13", prefixLen=24)
        net.getNodeByName("h4").setIP(ip="192.168.1.21", prefixLen=24)
        net.getNodeByName("h5").setIP(ip="192.168.1.22", prefixLen=24)
        net.getNodeByName("h6").setIP(ip="192.168.1.23", prefixLen=24)
        net.getNodeByName("h7").setIP(ip="192.168.1.31", prefixLen=24)
        net.getNodeByName("h8").setIP(ip="192.168.1.32", prefixLen=24)
        net.getNodeByName("h9").setIP(ip="192.168.1.33", prefixLen=24)
        net.getNodeByName("h10").setIP(ip="192.168.1.41", prefixLen=24)
        net.getNodeByName("h11").setIP(ip="192.168.1.42", prefixLen=24)
        net.getNodeByName("h12").setIP(ip="192.168.1.43", prefixLen=24)
        print("*** Executing background scripts")
    else:
        print("*** Executing background scripts and dhcp request")

    for h in net.hosts:
        if DHCP:
            h.cmd(f"sudo dhclient -4 -cf ./configs/mn_dhclient.conf") #+h.defaultIntf().name #-e HOST={str(h)}
        # With parantesesis invade the mininet terminal of single host and get signals
        h.cmd(f"python3 backgroundHost.py {str(h)} > {SDIR}/LOGs/{str(h)}.log &")
        # Start script slowly because jumps host if faster
        time.sleep(0.1)
        # net.terms += makeTerm(h, f"Background script on {str(h)}", cmd=f"python3 backgroundHost.py {str(h)}")
        print(f"Started {str(h)} script")
    print("All scripts started")

    # Run the summary status script NOT WORKING (not return the control to parent idk
    # command = f"xterm -T 'Status of all hosts' -e 'watch -n 1 python3 getStatusHosts.py'"
    # os.system(command + TONULL + " &")

    CLI(net)

    # After the user exits the CLI, shutdown the network.
    net.stop()
    shutil.rmtree(SDIR)


if __name__ == '__main__':
    # This runs if this file is executed directly
    setLogLevel( 'info' )
    runMinimalTopo()

# Allows the file to be imported using `mn --custom <filename> --topo minimal`
topos = {
    'minimal': MinimalTopo
}
