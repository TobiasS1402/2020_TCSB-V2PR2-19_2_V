#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter( Node ):

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):

    def build( self, **_opts ):
        r1 = self.addNode( 'r1', cls=LinuxRouter, ip='192.168.1.1/24' )
        s1, s2, s3, s4= [ self.addSwitch( s ) for s in ( 's1', 's2', 's3','s4') ]

        self.addLink( s1, r1, intfName2='r1-eth1', params2={ 'ip' : '192.168.1.1/24' } )
        self.addLink( s2, r1, intfName2='r1-eth2', params2={ 'ip' : '172.16.0.1/12' } )
        self.addLink( s3, r1, intfName2='r1-eth3', params2={ 'ip' : '10.0.0.1/8' } )
        self.addLink( s4, r1, intfName2='r1-eth4', params2={ 'ip' : '5.5.5.1/16' } )

        h1 = self.addHost( 'h1', ip='192.168.1.100/24', defaultRoute='via 192.168.1.1' )
        h2 = self.addHost( 'h2', ip='172.16.0.100/12', defaultRoute='via 172.16.0.1' )
        h3 = self.addHost( 'h3', ip='10.0.0.100/8', defaultRoute='via 10.0.0.1' )
        r2 = self.addNode( 'r2',cls=LinuxRouter,ip='5.5.5.100/16', defaultRoute='via 5.5.5.1' )

        for h, s in [ (h1, s1), (h2, s2), (h3, s3) ]:
            self.addLink( h, s)
        self.addLink(r2,s4)

topos = { 'mytopo': ( lambda: NetworkTopo() ) }
