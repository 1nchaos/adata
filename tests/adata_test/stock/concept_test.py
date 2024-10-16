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

    def test_get_concept_east_null(self):
        # 哈森股份，无题材测试
        stock_code = '603958'
        print(f"开始测试：get_concept_east:{stock_code}")
        df = adata.stock.info.get_concept_east(stock_code=stock_code)
        print(df)
        self.assertEqual(True, len(df) >= 0)

    def test_get_concept_east(self):
        # 中青旅
        stock_code = '600138'
        print(f"开始测试：get_concept_east:{stock_code}")
        df = adata.stock.info.get_concept_east(stock_code=stock_code)
        print(df)
        self.assertEqual(True, len(df) > 2)

    def test_get_plate_east(self):
        # 中青旅
        stock_code = '600138'
        print(f"开始测试：get_plate_east:{stock_code}")
        df = adata.stock.info.get_plate_east(stock_code=stock_code)
        print(df)
        self.assertEqual(True, len(df) > 2)


if __name__ == '__main__':
    unittest.main()
