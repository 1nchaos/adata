import unittest

import adata


class FundTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("----STAR执行:基金:函数测试用例STAR----")

    @classmethod
    def tearDownClass(cls) -> None:
        print("----END执行:基金:函数测试用例END----")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_all_etf_exchange_traded_info(self):
        print("开始测试：all_etf_exchange_traded_info")
        df = adata.fund.info.all_etf_exchange_traded_info()
        print(df)
        self.assertEqual(True, len(df) > 200)

    def test_get_market_etf(self):
        print("开始测试：get_market_etf")
        df = adata.fund.market.get_market_etf()
        print(df)
        self.assertEqual(True, len(df) > 200)

    def test_get_market_etf_min(self):
        print("开始测试：get_market_etf_min")
        df = adata.fund.market.get_market_etf_min()
        print(df)
        self.assertEqual(True, len(df) > 120)

    def test_get_market_etf_current(self):
        print("开始测试：get_market_etf_current")
        df = adata.fund.market.get_market_etf_current()
        print(df)
        self.assertEqual(True, len(df) == 1)


if __name__ == '__main__':
    unittest.main()
