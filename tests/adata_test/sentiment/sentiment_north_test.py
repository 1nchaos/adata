import unittest

import adata


class SentimentNorthTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("----STAR执行舆情-北向-函数测试用例STAR----")

    @classmethod
    def tearDownClass(cls) -> None:
        print("----END执行舆情-北向-函数测试用例END----")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_north_flow_current(self):
        print("开始测试：test_north_flow_current")
        df = adata.sentiment.north.north_flow_current()
        print(df)
        self.assertEqual(True, len(df) == 1)

    def test_north_flow_min(self):
        print("开始测试：test_securities_margin")
        df = adata.sentiment.north.north_flow_min()
        print(df)
        self.assertEqual(True, len(df) > 10)

    def test_north_flow(self):
        print("开始测试：test_north_flow")
        df = adata.sentiment.north.north_flow('2023-01-01')
        print(df)
        self.assertEqual(True, len(df) > 100)


if __name__ == '__main__':
    unittest.main()
