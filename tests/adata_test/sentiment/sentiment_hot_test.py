import unittest

import adata


class SentimentHotTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("----STAR执行舆情-热门-函数测试用例STAR----")

    @classmethod
    def tearDownClass(cls) -> None:
        print("----END执行舆情-热门-函数测试用例END----")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pop_rank_100_east(self):
        print("开始测试：pop_rank_100_east")
        df = adata.sentiment.hot.pop_rank_100_east()
        print(df)
        self.assertEqual(True, len(df) == 100)

    def test_hot_rank_100_ths(self):
        print("开始测试：hot_rank_100_ths")
        df = adata.sentiment.hot.hot_rank_100_ths()
        print(df)
        self.assertEqual(True, len(df) == 100)

    def test_hot_concept_20_ths(self):
        print("开始测试：hot_concept_20_ths")
        df = adata.sentiment.hot.hot_concept_20_ths()
        print(df)
        self.assertEqual(True, len(df) == 20)

    def test_list_a_list_daily(self):
        print("开始测试：list_a_list_daily")
        df = adata.sentiment.hot.list_a_list_daily(report_date='2024-07-04')
        print(df)
        self.assertEqual(True, len(df) >= 20)

    def test_get_a_list_info(self):
        print("开始测试：get_a_list_info")
        df = adata.sentiment.hot.get_a_list_info(stock_code='600297', report_date='2024-07-12')
        print(df)
        self.assertEqual(True, len(df) >= 10)


if __name__ == '__main__':
    unittest.main()
