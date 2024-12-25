# -*- coding: utf-8 -*-
"""
@desc: 
@author: 1nchaos
@time: 2023/7/2
@log: change log
"""
import unittest

import adata


class CapitalFlowTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("----STAR执行:资金流向:函数测试用例STAR----")

    @classmethod
    def tearDownClass(cls) -> None:
        print("----END执行:资金流向:函数测试用例END----")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_flow_min(self):
        print("开始测试：get_flow_min")
        df = adata.stock.market.get_capital_flow_min(stock_code='000001')
        print(df)
        self.assertEqual(True, len(df) > 0)

    def test_get_flow(self):
        print("开始测试：get_flow")
        df = adata.stock.market.get_capital_flow(stock_code='000001')
        print(df)
        self.assertEqual(True, len(df) > 200)

    def test_all_capital_flow_east(self):
        print("开始测试：all_capital_flow_east")
        df = adata.stock.market.all_capital_flow_east(days_type=1)
        print(df)
        self.assertEqual(True, len(df) > 200)


if __name__ == '__main__':
    unittest.main()
