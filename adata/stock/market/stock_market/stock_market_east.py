# -*- coding: utf-8 -*-
"""
@desc: 东方财富
https://quote.eastmoney.com/center/

@author: 1nchaos
@time: 2023/06/19
@log: change log
"""

import pandas as pd
from adata.common.exception.handler import handler_null

from adata.common.utils import requests
from adata.common.utils.date_utils import get_cur_time
from adata.stock.market.stock_market.stock_market_template import StockMarketTemplate


class StockMarketEast(StockMarketTemplate):
    """
    百度股票行情
    """

    def __init__(self) -> None:
        super().__init__()

    @handler_null
    def get_market(self, stock_code: str = '000001', start_date='1990-01-01', end_date=None, k_type=1,
                   adjust_type: int = 1):
        """
        :param stock_code: 6位股票代码
        :param start_date: 开始时间
        :param end_date: 结束日期
        :param k_type: k线类型：1.日；2.周；3.月
        :param adjust_type: k线复权类型：0.不复权；1.前复权；2.后复权 默认：1 前复权
        :return: k线行情数据:"时间戳", "时间","开盘","收盘","成交量","最高","最低","成交额","涨跌额","涨跌幅","换手率","昨收"
        """
        # 1. 参数处理
        se_cid = 1 if stock_code.startswith('6') else 0
        start_date = start_date.replace('-', '') if start_date else '19900101'
        end_date = end_date.replace('-', '') if end_date else get_cur_time("%Y%m%d")
        k_type = f"10{k_type}" if k_type < 5 else k_type
        params = {"fields1": "f1,f2,f3,f4,f5,f6",
                  "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f116",
                  "ut": "7eea3edcaed734bea9cbfc24409ed989",
                  "klt": k_type, "fqt": adjust_type,
                  "secid": f"{se_cid}.{stock_code}",
                  "beg": start_date, "end": end_date,
                  "_": "1623766962675",
                  }
        # 2. 请求url
        url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
        r = requests.request(method='get', url=url, params=params)
        data_json = r.json()

        # 3. 结果处理
        if not data_json["data"]:
            return pd.DataFrame()
        lines = data_json["data"]["klines"]
        if not lines:
            return pd.DataFrame()
        data = [item.split(",") for item in lines]
        df = pd.DataFrame(data=data, columns=["trade_date", "open", "close", "high", "low", "volume", "amount",
                                              '', "change_pct", "change", "turnover_ratio"])
        # 4.清洗数据
        df['pre_close'] = df['close'].astype(float) - df['change'].astype(float)
        df['trade_time'] = pd.to_datetime(df['trade_date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        df['trade_date'] = pd.to_datetime(df['trade_date']).dt.strftime('%Y-%m-%d')
        df['stock_code'] = stock_code
        numeric_columns = ['open', 'close', 'volume', 'high', 'low', 'amount', 'change', 'change_pct',
                           'turnover_ratio', 'pre_close']
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)
        df.reset_index(inplace=True, drop=True)
        return df[
            ['trade_time', "trade_date", "open", "close", "high", "low", "volume", "amount", "change_pct", "change",
             "turnover_ratio", "pre_close"]]

    @handler_null
    def get_market_min(self, stock_code: str = '000001'):
        """
        :param stock_code: 6位股票代码
        :return: k线行情数据:"时间","价格","涨跌率","涨幅","均价","成交量", "成交额"
        """
        #  # 1. 参数处理
        se_cid = 1 if stock_code.startswith('6') else 0
        params = {
            "fields1": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
            "ut": "fa5fd1943c7b386f172d6893dbfba10b",
            "ndays": "1", "iscr": "1",
            "iscca": "0", "secid": f"{se_cid}.{stock_code}",
            "_": "1623766962675",
        }
        url = "https://push2.eastmoney.com/api/qt/stock/trends2/get"
        res = requests.request(method='get', url=url, params=params).json()
        # 2. 结果处理
        if not res["data"]:
            return pd.DataFrame()

        # 3. 数据ETL
        pre_close = res["data"]["preClose"]
        data = [item.split(",") for item in res["data"]["trends"]]
        columns = ['trade_time', 'open', 'close', 'high', 'low', 'volume', 'amount', 'price']
        df = pd.DataFrame(data=data, columns=columns)
        # 前面的累加求和
        # df['avg_price'] = df['amount'].astype(float).cumsum() / df['volume'].astype(float).cumsum()/100
        # 换算成股
        df['volume'] = df['volume'].astype(float) * 100
        df['stock_code'] = stock_code
        df['avg_price'] = df['price']
        df['price'] = df['close']

        numeric_columns = ['open', 'close', 'volume', 'high', 'low', 'amount', 'price', 'avg_price']
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)

        df['change'] = df['price'] - pre_close
        df['change_pct'] = df['change'] / pre_close*100
        df['change_pct'] = df['change_pct'].round(2)
        df.reset_index(drop=True, inplace=True)
        return df[self._MARKET_MIN_COLUMNS]


if __name__ == '__main__':
    print(StockMarketEast().get_market(stock_code='600020', k_type=1, adjust_type=1))
    print(StockMarketEast().get_market_min(stock_code='600020'))
