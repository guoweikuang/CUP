#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright: [CUP] - See LICENSE for details.
# Authors: Yang Honggang
"""
:description:
    ut for cup.logging
"""
import os
import sys
import logging

_TOP = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/')
_TESTLOG = _TOP + '/testlog'
sys.path.insert(0, _TOP)

from cup import log, platforms
from cup import unittest

def test_gen_wf():
    """
    init_comlog指定ge_wf参数为True时，将大于等于WARING级别的消息
    写入${logfile}.wf日志文件中。本case用来验证相关功能是否符合
    预期。
    """
    logfile = _TESTLOG + '/cup.log'
    wflogfile = _TESTLOG + '/cup.log.wf'
    if os.path.exists(logfile):
        os.unlink(logfile)
    if os.path.exists(wflogfile):
        os.unlink(wflogfile)
    log.init_comlog(
        "log init", logging.DEBUG, logfile,
        log.ROTATION, gen_wf=True
    )


    log.info("info")
    log.critical("critical")
    log.error("error")
    log.warn("warning")
    log.debug("debug")

    # 检查是否生成了cup.log和cup.log.wf文件
    try:
        flog = open(logfile)
        flog_wf = open(wflogfile)
    except IOError:
        assert(False), "can not find cup.log or cup.log.wf file"
    # 检查cup.log的内容是否包括“debug”、"info"
    flog_str = flog.read()
    assert('debug' in flog_str and 'info' in flog_str), "cup.log's content error"
    # 检查cup.log.wf的内容是否包括"critical"、“error”和“warning”
    flog_wf_str = flog_wf.read()
    assert('critical' in flog_wf_str and 'error' in flog_wf_str and \
            'warning' in flog_wf_str), "cup.log.wf's content error"

    assert('debug' not in flog_wf_str and 'info' not in flog_wf_str), \
            "cup.log.wf's content error"
    # cup.log的内容不应该包括"critical"、“error”和“warning”
    assert('critical' in flog_str and 'error' in flog_str and \
            'warning' in flog_str), "cup.log's content error"


def test_log_parse():
    """cup.log.parse"""
    logline = ('INFO:    2023-01-04 22:29:25,456 +0800(CST) '
            '* [34666:115f70600] [log.py:327]'
        ' to compress folder into tarfile:'
    )
    kvs = log.parse(logline)
    unittest.assert_eq(kvs['loglevel'], 'INFO')
    unittest.assert_eq(kvs['date'], '2023-01-04')
    unittest.assert_eq(kvs['time'], '22:29:25,456')
    unittest.assert_eq(kvs['pid'], '34666')
    unittest.assert_eq(kvs['tid'], '115f70600')
    unittest.assert_eq(kvs['srcline'], 'log.py:327')
    unittest.assert_startswith(kvs['msg'], 'to compress')


def test_log_reinitcomlog():
    """test reinitcom log"""
    logfile = _TESTLOG + '/cup.new.log'
    log.reinit_comlog(
        "re init", logging.DEBUG, logfile,
        log.ROTATION, gen_wf=True
    )
    log.info("new info")
    log.critical("new critical")
    log.error("new error")
    log.warn("new warning")
    log.debug("new debug")


def _create_file(fname):
    """create file"""
    if not os.path.exists(fname):
        if platforms.is_linux():
            os.mknod(fname)
        else:
            with open(fname, 'w'):
                pass


def test_log_xfuncs():
    """test x log functions"""
    logxfile = _TESTLOG + '/cup.x.log'
    logyfile = _TESTLOG + '/cup.y.log'
    _create_file(logxfile)
    _create_file(logyfile)
    if not os.path.exists(logxfile):
        _create_file(logxfile)
    if not os.path.exists(logyfile):
        _create_file(logyfile)
    logparams = log.LoggerParams(
        log.DEBUG, logxfile, log.ROTATION, 100 * 1024 * 1024,
        True, True
    )

    log.xinit_comlog(logxfile, logparams)
    log.xdebug(logxfile, 'xdebug')
    log.xinfo(logxfile, 'xinfo')
    log.xerror(logxfile, 'xerror')
    logparams = log.LoggerParams(
        log.DEBUG, logyfile, log.ROTATION, 100 * 1024 * 1024,
        True, True
    )
    log.xinit_comlog(logyfile, logparams)
    log.xdebug(logyfile, 'ydebug')
    log.xinfo(logyfile, 'yinfo')
    log.xerror(logyfile, 'yerror')


def _main():
    test_gen_wf()
    test_log_parse()


if __name__ == '__main__':
    _main()

# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
