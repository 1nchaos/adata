# -*- coding: utf-8 -*-
"""
@desc: 
@author: 1nchaos
@time: 2023/7/2
@log: change log
"""
import unittest

import adata


class SentimentTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("----STAR执行:分红:函数测试用例STAR----")

    @classmethod
    def tearDownClass(cls) -> None:
        print("----END执行:分红:函数测试用例END----")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_dividend(self):
        print("开始测试：test_get_dividend")
        df = adata.stock.market.get_dividend(stock_code='000001')
        print(df)
        self.assertEqual(True, len(df) > 5)


if __name__ == '__main__':
    unittest.main()
