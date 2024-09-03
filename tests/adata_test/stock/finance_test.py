# -*- coding: utf-8 -*-
"""
@desc: 
@author: 1nchaos
@time: 2023/7/2
@log: change log
"""
import unittest

import adata


class FinanceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("----STAR执行:财务数据:函数测试用例STAR----")

    @classmethod
    def tearDownClass(cls) -> None:
        print("----END执行:财务数据:函数测试用例END----")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_core_index(self):
        print("开始测试：test_get_market_concept_ths")
        df = adata.stock.finance.get_core_index(stock_code='300059')
        print(df)
        self.assertEqual(True, len(df) > 30)


if __name__ == '__main__':
    unittest.main()