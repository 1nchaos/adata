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
        df = adata.stock.info.trade_calendar(year=2024)
        print(df)
        self.assertEqual(True, len(df) > 360)

    def test_all_concept_code_ths(self):
        print("开始测试：test_all_concept_code_ths")
        df = adata.stock.info.all_concept_code_ths()
        print(df)
        self.assertEqual(True, len(df) > 300)

    def test_concept_constituent_ths(self):
        print("开始测试：test_concept_constituent_ths")
        df = adata.stock.info.concept_constituent_ths(index_code="885556")
        print(df)
        self.assertEqual(True, len(df) > 200)

    def test_get_concept_ths(self):
        print("开始测试：get_concept_ths")
        df = adata.stock.info.get_concept_ths(stock_code="000002")
        print(df)
        self.assertEqual(True, len(df) > 6)

    def test_all_concept_code_east(self):
        print("开始测试：test_all_concept_code_ths")
        df = adata.stock.info.all_concept_code_east()
        print(df)
        self.assertEqual(True, len(df) > 300)

    def test_concept_constituent_east(self):
        print("开始测试：test_concept_constituent_ths")
        df = adata.stock.info.concept_constituent_east(concept_code="BK1104")
        print(df)
        self.assertEqual(True, len(df) > 200)

    def test_get_concept_east(self):
        print("开始测试：get_concept_ths")
        df = adata.stock.info.get_concept_east(stock_code="000002")
        print(df)
        self.assertEqual(True, len(df) > 6)

    def test_all_index_code(self):
        print("开始测试：test_all_index_code")
        df = adata.stock.info.all_index_code()
        print(df)
        self.assertEqual(True, len(df) > 500)

    def test_index_constituent(self):
        print("开始测试：test_index_constituent")
        df = adata.stock.info.index_constituent(index_code="000033")
        print(df)
        self.assertEqual(True, len(df) > 10)


if __name__ == '__main__':
    unittest.main()
