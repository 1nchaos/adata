# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/7/5
@log: change log
"""
import unittest

import adata


class BondTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("----STAR执行:债券:函数测试用例STAR----")

    @classmethod
    def tearDownClass(cls) -> None:
        print("----END执行:债券:函数测试用例END----")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_all_convert_code(self):
        print("开始测试：all_convert_code")
        df = adata.bond.info.all_convert_code()
        print(df)
        self.assertEqual(True, len(df) > 200)


if __name__ == '__main__':
    unittest.main()
