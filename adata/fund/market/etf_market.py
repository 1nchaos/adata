# -*- coding: utf-8 -*-
"""
@desc: ETF 行情
@author: 1nchaos
@time:2023/4/5
@log: 
"""
from adata.fund.market.etf_market_ths import ETFMarketThs


class ETFMarket(object):
    """ETF 行情"""

    def __init__(self) -> None:
        super().__init__()
        self.ths = ETFMarketThs()

    def get_market_etf(self, fund_code: str = '512880', k_type: int = 1, start_date='', end_date=''):
        """
        获取ETF的行情
        :param start_date: 开始时间
        :param end_date: 结束时间
        :param fund_code: ETF代码
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :return: k线行情数据 [日期，开，高，低，收,成交量，成交额]
        ;20230419,958.901,981.118,958.449,961.107,521143220,20442229000.000
        成交量：股 820953530  821万手
        成交额：元 16959251000.000 169.6亿
        """
        return self.ths.get_market_etf_ths(fund_code, k_type, start_date, end_date)

    def get_market_etf_min(self, fund_code='512880'):
        """
        获取etf行情当日分时
        :param fund_code: ETF代码
        :return 时间，现价，成交额（元），均价，成交量（股） 涨跌额，涨跌幅
        'index_code', 'trade_time', 'price', 'change', 'change_pct', 'volume', 'pre_close', 'amount'
        """
        return self.ths.get_market_etf_min_ths(fund_code)

    def get_market_etf_current(self, fund_code: str = '512880', k_type: int = 1):
        """
        获取同花顺当前的概念行情

        :param fund_code: ETF代码
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :return: k线行情数据 [ETF代码,交易时间，交易日期，开，高，低，当前价格,成交量，成交额]
        ;20230419,958.901,981.118,958.449,961.107,521143220,20442229000.000,存储芯片
        k:   1,      7,      8,       9,      11,      13,         19,        name
        成交量：股 820953530  821万手
        成交额：元 16959251000.000 169.6亿
        """
        return self.ths.get_market_etf_current_ths(fund_code, k_type)


if __name__ == '__main__':
    print(ETFMarket().get_market_etf(fund_code='159529', start_date='2024-01-01'))
    print(ETFMarket().get_market_etf_min(fund_code='159529'))
    print(ETFMarket().get_market_etf_current(fund_code='512880'))
