import unittest

import adata


class SentimentTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("----STAR执行舆情函数测试用例STAR----")

    @classmethod
    def tearDownClass(cls) -> None:
        print("----END执行舆情函数测试用例END----")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_stock_lifting_last_month(self):
        print("开始测试：test_stock_lifting_last_month")
        df = adata.sentiment.stock_lifting_last_month()
        print(df)
        self.assertEqual(True, len(df) > 1)

    def test_securities_margin(self):
        print("开始测试：test_securities_margin")
        df = adata.sentiment.securities_margin(start_date='2020-01-01')
        print(df)
        self.assertEqual(True, len(df) > 250)

    def test_hot_rank_100_ths(self):
        print("开始测试：hot_rank_100_ths")
        df = adata.sentiment.hot.hot_rank_100_ths()
        print(df)
        self.assertEqual(True, len(df) == 100)

    def test_pop_rank_100_east(self):
        print("开始测试：pop_rank_100_east")
        df = adata.sentiment.hot.pop_rank_100_east()
        print(df)
        self.assertEqual(True, len(df) == 100)

    def test_hot_concept_20_ths(self):
        print("开始测试：hot_concept_20_ths")
        df = adata.sentiment.hot.hot_concept_20_ths()
        print(df)
        self.assertEqual(True, len(df) == 20)


if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    # unittest.main
    suite = unittest.TestSuite()
    caseList = ["test_stock_lifting_last_month"]
    for case in caseList:
        suite.addTest(SentimentTestCase(case))
    # 运行测试用例
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
