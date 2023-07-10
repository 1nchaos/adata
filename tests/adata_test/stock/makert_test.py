# -*- coding: utf-8 -*-
"""
@summary:
@author: 1nchaos
@date: 2023/7/2 07:51
"""
import unittest

import adata


class MarketTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("----STAR执行:行情:函数测试用例STAR----")

    @classmethod
    def tearDownClass(cls) -> None:
        print("----END执行:行情:函数测试用例END----")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_market(self):
        print("开始测试：test_get_market")
        df = adata.stock.market.get_market(stock_code='000001', start_date='2021-01-01', k_type=1)
        print(df)
        self.assertEqual(True, len(df) > 300)

    def test_get_market_min(self):
        print("开始测试：test_get_market_min")
        df = adata.stock.market.get_market_min(stock_code='000001')
        print(df)
        self.assertEqual(True, len(df) > 1)

    def test_list_market_current(self):
        print("开始测试：test_get_market_min")
        df = adata.stock.market.list_market_current(code_list=['000001', '600001', '000795', '872925'])
        print(df)
        self.assertEqual(True, len(df) > 2)


if __name__ == '__main__':
    unittest.main()
