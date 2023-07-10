# -*- coding: utf-8 -*-
"""
@desc: 
@author: 1nchaos
@time: 2023/7/2
@log: change log
"""
import unittest

import adata


class MarketIndexTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("----STAR执行:指数行情:函数测试用例STAR----")

    @classmethod
    def tearDownClass(cls) -> None:
        print("----END执行:指数行情:函数测试用例END----")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_market_index(self):
        print("开始测试：get_market_index")
        df = adata.stock.market.get_market_index(index_code='000001')
        print(df)
        self.assertEqual(True, len(df) > 30)

    def test_get_market_index_min(self):
        print("开始测试：get_market_index_min")
        df = adata.stock.market.get_market_index_min(index_code='000001')
        print(df)
        self.assertEqual(True, len(df) > 2)

    def test_get_market_index_current(self):
        print("开始测试：get_market_index_current")
        df = adata.stock.market.get_market_index_current(index_code='000001')
        print(df)
        self.assertEqual(True, len(df) > 0)


if __name__ == '__main__':
    unittest.main()
