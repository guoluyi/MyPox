#!/usr/bin/python

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

def addHost (net, N, ip = None):
    name = 'h%d' % N
    if ip is None:
      ip = '10.0.0.%d' % N
    return net.addHost(name, ip=ip)

def makeNet ():
    net = Mininet()
     
    hosts = [ addHost(net, n+1, ip) for n,ip in
              enumerate("10.0.0.1 0.0.0.0 10.0.0.2".split()) ]
  
    for h1,h2 in zip(hosts[:-1],hosts[1:]):
      h1.linkTo(h2)

    net.build()

    # Execute commands on h2...
    hosts[1].cmd('ifconfig h2-eth0 0.0.0.0 up')
    hosts[1].cmd('ifconfig h2-eth1 0.0.0.0 up')
    hosts[1].cmd('~/pox_carp/pox.py datapaths.pcap_switch '
                 '--ports=h2-eth0,h2-eth1 forwarding.l2_pairs &')
    
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    makeNet()
