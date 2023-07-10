# -*- coding: utf-8 -*-
"""
@desc: 
@author: 1nchaos
@time: 2023/7/2
@log: change log
"""
import time
import unittest

import adata


class MarketConceptTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("----STAR执行:概念行情:函数测试用例STAR----")

    @classmethod
    def tearDownClass(cls) -> None:
        print("----END执行:概念行情:函数测试用例END----")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_market_concept_ths(self):
        print("开始测试：test_get_market_concept_ths")
        time.sleep(5)
        df = adata.stock.market.get_market_concept_ths(index_code='886041')
        print(df)
        self.assertEqual(True, len(df) > 30)

    def test_get_market_concept_min_ths(self):
        print("开始测试：test_get_market_concept_min_ths")
        time.sleep(5)
        df = adata.stock.market.get_market_concept_min_ths(index_code='886041')
        print(df)
        self.assertEqual(True, len(df) > 2)

    def test_get_market_concept_current_ths(self):
        print("开始测试：test_get_market_concept_current_ths")
        time.sleep(5)
        df = adata.stock.market.get_market_concept_current_ths(index_code='886041')
        print(df)
        self.assertEqual(True, len(df) > 0)


if __name__ == '__main__':
    unittest.main()
