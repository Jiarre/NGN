import os
import shutil
import time

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, OVSSwitch
from mininet.term import makeTerm

SDIR = "/tmp/NGN/hosts"
TONULL = "&>/dev/null"

class MinimalTopo( Topo ):

    def build( self ):
        hosts = []
        h1 = self.addHost( 'h1' , ip="192.168.1.11" )
        h2 = self.addHost( 'h2', ip="192.168.1.12" )
        h3 = self.addHost( 'h3', ip="192.168.1.13" )
        h4 = self.addHost( 'h4', ip="192.168.1.21" )
        h5 = self.addHost( 'h5' , ip="192.168.1.22" )
        h6 = self.addHost( 'h6', ip="192.168.1.23" )
        h7 = self.addHost( 'h7', ip="192.168.1.31" )
        h8 = self.addHost( 'h8', ip="192.168.1.32" )
        h9 = self.addHost( 'h9' , ip="192.168.1.33" )
        h10 = self.addHost( 'h10', ip="192.168.1.41" )
        h11 = self.addHost( 'h11', ip="192.168.1.42" )
        h12 = self.addHost( 'h12', ip="192.168.1.43" )

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

        if os.path.exists(SDIR):
            shutil.rmtree(SDIR)
        # os.makedirs(SDIR) #recursive
        os.makedirs(f"{SDIR}/LOGs", 0o777)
        os.environ["statusdir"] = SDIR

        for i in range(1, len(hosts) + 1):
            host = "h" + str(i)
            file = SDIR + "/" + host
            # Set status file
            try:
                f = open(os.open(file, os.O_CREAT | os.O_WRONLY, 0o777), 'w')
                if i == 1:
                    # Only h1 stars UP
                    f.write("UP")
                else:
                    f.write("DOWN")
                f.close()
            except OSError:
                print("Failed creating the file")
            else:
                print("File " + file + " created")


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

    print("*** Executing background scripts")
    for h in net.hosts:
        # Not work because not return control to mininet
        # command = f"xterm -T 'Background script on {str(h)}' -e 'python3 backgroundHost.py {str(h)};'"
        # h.cmd(command + TONULL + " &")   # & for no-wait execution #>{SDIR}/LOGs/{str(h)}.log
        # umask 0;
        h.cmd(f"python3 backgroundHost.py {str(h)} {SDIR}/LOGs/{str(h)}.log &")
        # Start script slowly because jumps host if faster
        time.sleep(0.01)
        # net.terms += makeTerm(h, f"Background script on {str(h)}", cmd=f"python3 backgroundHost.py {str(h)}")
        print(f"Stated {str(h)} script")
    print("All scripts stated")

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
