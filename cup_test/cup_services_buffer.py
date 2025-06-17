#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright: [CUP] - See LICENSE for details.
# Authors: Guannan Ma (@mythmgn),
"""
:description:
    unittest for cup.services.buffers
"""
from cup.services import buffers
from cup import unittest
import unittest as sysut


class TestServiceBuffer(sysut.TestCase):
    """
    service buffer
    """
    def setUp(self):
        """
        setup
        """
        self.buffpool = buffers.BufferPool(
            102400,
            buffers.MEDIUM_BLOCK_SIZE, False
        )

    def tearDown(self):
        """
        teardown
        """
        pass

    def test_buffalloc(self):
        """test_run"""
        ret, buff = self.buffpool.allocate(102401)
        unittest.assert_eq(ret, False)
        ret, buff = self.buffpool.allocate(10)
        unittest.assert_eq(ret, True)
        # pylint: disable=W0212
        unittest.assert_eq(self.buffpool._used_num, 10)
        unittest.assert_eq(self.buffpool._free_num, 102390)
        ret = buff.set('a' * 10 * buffers.MEDIUM_BLOCK_SIZE)
        unittest.assert_eq(ret[0], True)
        ret = buff.set('a' * (10 * buffers.MEDIUM_BLOCK_SIZE + 1))
        unittest.assert_ne(ret[0], True)
        self.buffpool.deallocate(buff)
        # pylint: disable=W0212
        unittest.assert_eq(self.buffpool._used_num, 0)
        unittest.assert_eq(self.buffpool._free_num, 102400)
        unittest.assert_eq(len(self.buffpool._free_list), 102400)
        unittest.assert_eq(len(self.buffpool._used_dict), 0)


# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
