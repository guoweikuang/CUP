#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright: [CUP] - See LICENSE for details.
# Authors: Guannan Ma (@mythmgn),
"""
:description:
    unittest for cup.cache
"""
import time
import unittest
import threading

from cup import cache


# def test_cache_basic_set_get():
#     """test basic cache set/get"""
#     kvcache = cache.KVCache('basic_test')
#     kvcache.set(
#         {
#             'test-0': 'test_value0',
#             'test-1': 'test_value1'
#         }
#     )
#     kvcache.get('test-0')
#     unittest.assert_eq(kvcache.get('test-0'), 'test_value0')
#     kvcache.set(
#         {
#             'test-0': 'test_value0',
#             'test-1': 'test_value1'
#         },
#         2
#     )
#     time.sleep(3)
#     unittest.assert_eq(kvcache.get('test-0'), None)
#     unittest.assert_eq(kvcache.get('test-1'), None)


# def test_cache_refresh_with_get():
#     """
#     test cache refresh
#     """
#     kvcache = cache.KVCache('basic_test', 5)
#     kvcache.set_time_extension(3)
#     kvcache.set(
#         {
#             'test-0': 'test_value0',
#             'test-1': 'test_value1'
#         },
#         2
#     )
#     time.sleep(1)
#     kvcache.get('test-0')
#     time.sleep(2)
#     assert kvcache.get('test-0') == 'test_value0'
#     assert kvcache.get('test-1') is None


# def test_cache_replace():
#     """test cache replace"""
#     kvcache = cache.KVCache('basic_test', 3)
#     kvcache.set_time_extension(3)
#     assert not kvcache.set(
#         {
#             'test-0': 'test_value0',
#             'test-1': 'test_value1',
#             'test-2': 'test_value1',
#             'test-3': 'test_value1'
#         },
#         2
#     )
#     kvcache.set(
#         {
#             'test-0': 'test_value0',
#             'test-1': 'test_value1',
#             'test-2': 'test_value1',
#         },
#         1
#     )
#     assert kvcache.set({'test-3':'test_value3'}, 2) is True
#     # print(kvcache._kv_data)
#     assert kvcache.get('test-0') is None
#     assert kvcache.get('test-3') == 'test_value3'
#     time.sleep(2)
#     # print(kvcache._kv_data)
#     assert kvcache.get('test-3') == 'test_value3'
#     kvcache.set({'test-4': 'test_value4'}, 1)
#     kvcache.set({'test-5': 'test_value5'}, 1)
#     # print(kvcache._kv_data)


# def test_cache_getexpired():
#     """test get expired"""
#     kvcache = cache.KvCache('basic_test', 5)
#     kvcache.set_time_extension(3)
#     kvcache.set({'k0': 'v0'}, 1)
#     kvcache.set({'k1': 'v1'}, 1)
#     kvcache.set({'k1': 'v1'}, 50)
#     kvcache.get('k1')
#     time.sleep(2)
#     # print(kvcache.pop_n_expired(1)
#     assert kvcache.pop_n_expired(1).get('k0') is not None
#     time.sleep(3)
#     # print(kvcache.pop_n_expired())
#     assert kvcache.pop_n_expired(1).get('k1') is not None


import unittest
from cup.cache import KVCache

class TestKVCache(unittest.TestCase):

    def setUp(self):
        self.cache = KVCache()

    def test_set_and_get(self):
        # 测试设置和获取单个键值对
        self.cache.set({'key1': 'value1'}, expire_sec=10)
        value = self.cache.get('key1')
        self.assertEqual(value, 'value1')

    def test_set_multiple(self):
        # 测试设置多个键值对
        kvdict = {'key2': 'value2', 'key3': 'value3'}
        self.cache.set(kvdict, expire_sec=10)
        value2 = self.cache.get('key2')
        value3 = self.cache.get('key3')
        self.assertEqual(value2, 'value2')
        self.assertEqual(value3, 'value3')

    def test_replace(self):
        # 测试替换已存在的键值对
        self.cache.set({'key1': 'value1'}, expire_sec=10)
        replaced_value = self.cache.replace('key1', 'new_value1', ex=10)
        self.assertEqual(replaced_value, 'new_value1')

    def test_get_expired(self):
        # 测试获取已过期的键值对
        self.cache.set({'key1': 'value1'}, expire_sec=1)
        time.sleep(2)
        value = self.cache.get('key1')
        self.assertIsNone(value)

    def test_pop_n_expired(self):
        # 测试弹出多个过期的键值对
        kvdict = {'key2': 'value2', 'key3': 'value3'}
        self.cache.set(kvdict, expire_sec=1)
        time.sleep(2)
        expired_items = self.cache.pop_n_expired(num=2)
        self.assertEqual(len(expired_items), 2)

    def test_size(self):
        # 测试缓存大小
        self.cache.set({'key1': 'value1'}, expire_sec=10)
        self.assertEqual(self.cache.size(), 1)

    def test_clear(self):
        # 测试清除缓存
        self.cache.set({'key1': 'value1'}, expire_sec=10)
        self.cache.clear()
        self.assertEqual(self.cache.size(), 0)

    def test_expire(self):
        # 测试设置键的过期时间
        self.cache.set({'key1': 'value1'}, expire_sec=10)
        self.cache.expire('key1', ex=1)
        time.sleep(2)
        value = self.cache.get('key1')
        self.assertIsNone(value)

    def test_mapupdate(self):
        # 测试更新键对应的值字典
        self.cache.set({'key1': {'subkey1': 'value1'}}, expire_sec=10)
        self.cache.mapupdate('key1', {'subkey2': 'value2'}, ex=10)
        value = self.cache.get('key1')
        if value is not None:
            self.assertIn('subkey2', value)
        else:
            self.fail("key1 not found in cache, failed to mapupdate")

    def test_thread_safety(self):
        def worker(cache, lock):
            for i in range(3):
                with lock:
                    cache.set({f"key{i}": f"value{i}"})
                    time.sleep(0.1)  # Small delay to simulate real-world conditions

        lock = threading.Lock()
        threads = [threading.Thread(target=worker, args=(self.cache, lock)) for _ in range(5)]
        
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        self.assertEqual(self.cache.size(), 3)  # Assuming maxsize is 3 and all threads are done
    
    def test_cache_expire_setup(self):
        kvcache = cache.KVMemCache('basic_test', 3)
        kvcache.set_time_extension(3)
        kvcache.set({'k0': 'v0'}, 10)
        kvcache.set({'k1': 'v1'}, 11)
        kvcache.set({'k2': 'v2'}, 50)
        kvcache.set({'k3': 'v3'}, 20)

        assert kvcache.get('k0') is None
        assert kvcache.get('k1') == 'v1'
        assert kvcache.get('k2') == 'v2'
        kvcache.expire('k2', 2)
        time.sleep(3)
        # k2 is Gone
        assert kvcache.get('k2') is None    
        print(kvcache.pop_n_expired(1))
        kvcache.set({'k4': 'v4'}, 3)
        kvcache.set({'k4': 'v4'}, 3)


if __name__ == '__main__':
    unittest.main()


# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
