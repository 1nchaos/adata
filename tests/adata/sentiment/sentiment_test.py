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
