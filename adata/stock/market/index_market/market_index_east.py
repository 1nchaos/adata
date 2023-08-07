# -*- coding: utf-8 -*-
"""
@summary: 股票指数 行情
@author: 1nchaos
@date: 2023/06/01 16:17
"""
import datetime

import pandas as pd

from adata.common import requests
from adata.stock.market.index_market.market_index_template import StockMarketIndexTemplate


class StockMarketIndexEast(StockMarketIndexTemplate):
    def __init__(self) -> None:
        super().__init__()

    def get_market_index(self, index_code: str = '000001', start_date='2020-01-01', k_type: int = 1):
        """
        获取指数行情
        http://77.push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.000300&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=102&fqt=1&beg=0&end=20500101&smplmt=1247.73&lmt=1000000
        :param start_date: 开始时间
        :param index_code: 指数代码
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :return: k线行情数据 [日期，开，高，低，收,成交量，成交额]
        """
        url = f"http://77.push2his.eastmoney.com/api/qt/stock/kline/get?" \
              f"secid=1.{index_code}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&" \
              f"klt=10{k_type}&fqt=1&beg=0&end=20500101&smplmt=1247.73&lmt=1000000"
        res_json = requests.request('get', url, headers={}, proxies={}).json()
        # 解析数据
        code = res_json['data']['code']
        if code != index_code:
            return
        res_data = res_json['data']['klines']
        data = []
        for _ in res_data:
            row = str(_).split(',')
            data.append(
                {'trade_date': row[0], 'open': row[1], 'close': row[2], 'high': row[3], 'low': row[4], 'volume': row[5],
                 'amount': row[6], 'change': row[9], 'change_pct': row[8], 'index_code': index_code})
        result_df = pd.DataFrame(data=data, columns=self._MARKET_INDEX_COLUMNS)

        # 清洗数据
        result_df[['open', 'high', 'low', 'close', 'volume', 'amount', 'change', 'change_pct']] = \
            result_df[['open', 'high', 'low', 'close', 'volume', 'amount', 'change', 'change_pct']].astype(float)
        result_df['trade_time'] = pd.to_datetime(result_df['trade_date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        result_df = result_df.round(2)
        if start_date:
            result_df = result_df[result_df['trade_date'] >= start_date]
        return result_df[self._MARKET_INDEX_COLUMNS]

    def get_market_index_min(self, index_code='000001'):
        """
        获取指数当日的分时行情
        http://push2his.eastmoney.com/api/qt/stock/trends2/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58&iscr=0&ndays=1&secid=1.000300
        :param index_code: 指数代码
        :return 时间，现价，成交额（元），均价，成交量（股） 涨跌额，涨跌幅
        ['index_code', 'trade_time', 'price', 'change', 'change_pct', 'volume', 'avg_price', 'amount']
        """
        url = f"http://push2his.eastmoney.com/api/qt/stock/trends2/get?" \
              f"fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58&" \
              f"iscr=0&ndays=1&secid=1.{index_code}"
        res_json = requests.request('get', url, headers={}, proxies={}).json()
        # 解析数据
        code = res_json['data']['code']
        pre_price = res_json['data']['prePrice']
        if code != index_code:
            return
        res_data = res_json['data']['trends']
        data = []
        for _ in res_data:
            row = str(_).split(',')
            data.append(
                {'trade_date': row[0], 'open': row[1], 'close': row[2], 'high': row[3], 'low': row[4],
                 'volume': row[5], 'amount': row[6], 'avg_price': row[7], 'index_code': index_code})
        result_df = pd.DataFrame(data=data, columns=self._MARKET_INDEX_MIN_COLUMNS)

        # 清洗数据
        result_df[['open', 'high', 'low', 'close', 'volume', 'amount', 'avg_price']] = \
            result_df[['open', 'high', 'low', 'close', 'volume', 'amount', 'avg_price']].astype(float)
        result_df['trade_time'] = pd.to_datetime(result_df['trade_date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        result_df['change'] = result_df['close'] - pre_price
        result_df['change_pct'] = result_df['change'] / pre_price * 100
        result_df = result_df.round(2)
        return result_df

    def get_market_index_current(self, index_code: str = '000001'):
        """
        获取当前的指数行情
        :param index_code: 指数代码
        :return: [指数代码,交易时间，交易日期，开，高，低，当前价格,成交量，成交额]
        ['trade_time', 'trade_date', 'open', 'high', 'low', 'price', 'volume', 'amount']
        """
        url = f"http://push2.eastmoney.com/api/qt/stock/get?" \
              f"invt=2&fltt=1&fields=f58,f107,f57,f43,f59,f169,f170,f152,f46,f60,f44,f45,f47,f48,f19,f532,f39,f161,f49," \
              f"f171,f50,f86,f600,f601,f154,f84,f85,f168,f108,f116,f167,f164,f92,f71,f117,f292,f113,f114,f115,f119," \
              f"f120,f121,f122,f296&secid=1.{index_code}&wbp2u=|0|0|0|web"
        res_json = requests.request('get', url, headers={}, proxies={}).json()
        # 解析数据
        j = res_json['data']
        if not j:
            return pd.DataFrame(data=[], columns=self._MARKET_INDEX_CURRENT_COLUMNS)
        code = j['f57']
        if code != index_code:
            return pd.DataFrame(data=[], columns=self._MARKET_INDEX_CURRENT_COLUMNS)
        pre_close = j['f60']
        data = [{'open': j['f46'], 'high': j['f44'], 'low': j['f45'], 'price': j['f43'], 'volume': j['f47'],
                 'amount': j['f48'], 'index_code': index_code}]
        result_df = pd.DataFrame(data=data, columns=self._MARKET_INDEX_CURRENT_COLUMNS)

        # 清洗数据
        result_df[['open', 'high', 'low', 'price', 'volume', 'amount']] = \
            result_df[['open', 'high', 'low', 'price', 'volume', 'amount']].astype(float)
        result_df['change'] = result_df['price'] - pre_close
        result_df['change_pct'] = result_df['change'] / pre_close * 100
        result_df = result_df.round(2)
        # result_df['trade_time'] = datetime.datetime.now()
        return result_df


if __name__ == '__main__':
    # print(StockMarketIndexEast().get_market_index(index_code='000001', start_date='2022-12-01'))
    # print(StockMarketIndexEast().get_market_index_min(index_code='000001'))
    print(StockMarketIndexEast().get_market_index_current(index_code='000001'))
