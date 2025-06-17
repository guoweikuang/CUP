#!/bin/env python
# -*- coding: utf-8 -*
"""
    Author: (Guannan Ma)
"""

import os
import sys
import pdb
import unittest as sysunit
import socket

_NOW_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.insert(0, _NOW_PATH + '../')

from cup import net
from cup.net import route
from cup import platforms
from cup import unittest


class TestNetInit(sysunit.TestCase):
    def test_port_free(self):
        """test port_listened"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0', 61113))
        sock.settimeout(1)
        net.set_sock_reusable(sock)
        sock.listen(1)
        ret = net.localport_free(61113)
        unittest.assert_eq(ret, False)
        unittest.assert_eq(
            net.port_listened(net.get_local_hostname(), 61113),
            True
        )
        sock.close()
    
    def test_get_interfacebyip(self):
        """test get_interfacebyip"""
        """test """
        if platforms.is_linux():
            robj = route.RouteInfo()
            unittest.assert_eq(robj.get_interface_by_ip('127.0.0.1'), 'lo')


if __name__ == '__main__':
    sysunit.main()

# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
