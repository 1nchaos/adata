# -*- coding: utf-8 -*-
import unittest

import adata


class InfoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("----STAR执行：股票：信息：函数测试用例STAR----")

    @classmethod
    def tearDownClass(cls) -> None:
        print("----END执行：股票：信息：函数测试用例END----")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_all_code(self):
        print("开始测试：test_all_code")
        df = adata.stock.info.all_code()
        print(df)
        self.assertEqual(True, len(df) > 4000)

    def test_trade_calendar(self):
        print("开始测试：test_trade_calendar")
        df = adata.stock.info.trade_calendar(year=2023)
        print(df)
        self.assertEqual(True, len(df) > 360)

    def test_all_concept_code_ths(self):
        print("开始测试：test_all_concept_code_ths")
        df = adata.stock.info.all_concept_code_ths()
        print(df)
        self.assertEqual(True, len(df) > 300)

    def test_all_index_code(self):
        print("开始测试：test_all_index_code")
        df = adata.stock.info.all_index_code()
        print(df)
        self.assertEqual(True, len(df) > 500)


if __name__ == '__main__':
    unittest.main()
