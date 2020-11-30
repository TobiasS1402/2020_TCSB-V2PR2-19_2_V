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
        r1 = self.addNode( 'r1', cls=LinuxRouter, ip='5.5.5.5/24' )
        s1, s2, s3 = [ self.addSwitch( s ) for s in ( 's1', 's2', 's3') ]

        self.addLink( s1, r1, intfName2='r1-eth1', params2={ 'ip' : '10.1.1.0/24' } )
        self.addLink( s2, r1, intfName2='r1-eth2', params2={ 'ip' : '192.168.1.0/24' } )
        self.addLink( s3, r1, intfName2='r1-eth3', params2={ 'ip' : '172.16.0.0/24' } )

        msp_a = self.addHost( 'msp_a', ip='10.1.1.2/24', defaultRoute='via 10.1.1.1' )
        msp_b = self.addHost( 'msp_b', ip='10.1.1.3/24', defaultRoute='via 10.1.1.1' )
        klanta_a = self.addHost( 'klanta_a', ip='192.168.1.2/248', defaultRoute='via 192.168.1.1' )
        klanta_b = self.addHost( 'klanta_b', ip='192.168.1.3/24', defaultRoute='via 192.168.1.1' )
        klantc_a = self.addHost( 'klantc_a', ip='172.16.0.2/24', defaultRoute='via 172.16.0.1' )
        klantc_b = self.addHost( 'klantc_b', ip='172.16.0.3/24', defaultRoute='via 172.16.0.1' )
        for h, s in [ (msp_a, s1), (msp_b, s1), (klanta_a, s2), (klanta_b, s2), (klantc_a, s3), (klantc_b, s3) ]:
            self.addLink( h, s)

topos = { 'mytopo': ( lambda: NetworkTopo() ) }
