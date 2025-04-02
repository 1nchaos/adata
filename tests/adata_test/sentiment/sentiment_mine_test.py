import unittest

import adata


class SentimentMineTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("----STAR执行舆情-扫雷-函数测试用例STAR----")

    @classmethod
    def tearDownClass(cls) -> None:
        print("----END执行舆情-扫雷-函数测试用例END----")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mine_clearance_tdx(self):
        print("开始测试：mine_clearance_tdx")
        df = adata.sentiment.mine.mine_clearance_tdx()
        print(df)
        self.assertEqual(True, len(df) >= 10)


if __name__ == '__main__':
    unittest.main()
