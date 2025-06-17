#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright: [CUP] - See LICENSE for details.
# Authors: Guannan Ma (@mythmgn),
"""
:description:
    unittest for cup.services.executor
"""
import os
import sys
import time
import unittest as sysut

_TOP = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/')
sys.path.insert(0, _TOP + '../')
_TESTLOG = _TOP + 'testlog'


import cup
from cup import unittest
from cup import log
from cup.services import executor


class TestMyCase(sysut.TestCase):
    """
    test class for cup
    """

    def setUp(self):
        """
        setup
        """
        log.init_comlog('executor_test', log.DEBUG, _TESTLOG, log.ROTATION, 1024*1024*10, False, True)
        self._executor = executor.ExecutionService(
        )
        self._executor.run()
        self._info = time.time()

    def _change_data(self, data=None):
        self._info = time.time() + 100

    def test_run(self):
        """
        @author: maguannan
        """
        self._executor.delay_exec(5, self._change_data, 1)
        time.sleep(2)
        assert time.time() > self._info
        time.sleep(5)
        assert time.time() < self._info

    def tearDown(self):
        """
        teardown
        """
        cup.log.info('End running ' + str(__file__))
        self._executor.stop()

if __name__ == '__main__':
    cup.unittest.CCaseExecutor().runcase(TestMyCase())

# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent

