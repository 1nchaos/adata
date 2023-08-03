# -*- coding: utf-8 -*-
"""
@summary: 股票概念 行情
https://quote.eastmoney.com/bk/90.BK0612.html
TODO 概念板块当日涨跌幅排名
https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=1000&po=1&fid=f3&fields=f1,f2,f3,f4,f12,f13,f14&fs=b:BK0900&ut=fa5fd1943c7b386f172d6893dbfba10b&cb=jQuery35109553587682356608_1691083378045&_=1691083378046
@author: 1nchaos
@date: 2023/08/03 23:17
"""
import pandas as pd

from adata.common import requests


class ConceptMarketEase(object):
    """
    股票概念 行情
    """
    __MARKET_COLUMNS = ['index_code', 'trade_time', 'trade_date', 'open', 'high', 'low', 'close', 'volume',
                        'amount', 'change', 'change_pct']
    __MARKET_CONCEPT_MIN_COLUMNS = ['index_code', 'trade_time', 'trade_date', 'open', 'high', 'low', 'close', 'volume',
                                    'amount', 'change', 'change_pct', 'avg_price']
    __MARKET_CONCEPT_CURRENT_COLUMNS = ['index_code', 'trade_time', 'trade_date', 'open', 'high', 'low', 'price',
                                        'volume', 'amount', 'change', 'change_pct']

    def get_market_concept_east(self, index_code: str = 'BK0612', k_type: int = 1):
        """
        获取东方财富的概念的行情
        https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=90.BK0612&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=1&end=20500101&lmt=1000000
        :param index_code: 东方财富概念指数代码：BK开头
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :return: k线行情数据 [日期，开，高，低，收,成交量，成交额]
         "2012-06-14,765.93,760.75,766.05,759.93,28427953,30155329024.00,0.61,-23.93,-239.25,0.12",
        成交量：股 820953530  821万手
        成交额：元 16959251000.000 169.6亿
        """
        url = f"https://push2his.eastmoney.com/api/qt/stock/kline/get?" \
              f"secid=90.{index_code}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61" \
              f"&klt=10{k_type}&fqt=1&end=20500101&lmt=1000000"
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
        result_df = pd.DataFrame(data=data, columns=self.__MARKET_COLUMNS)

        # 清洗数据
        result_df[['open', 'high', 'low', 'close', 'volume', 'amount', 'change', 'change_pct']] = \
            result_df[['open', 'high', 'low', 'close', 'volume', 'amount', 'change', 'change_pct']].astype(float)
        result_df['trade_time'] = pd.to_datetime(result_df['trade_date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        result_df = result_df.round(2)
        return result_df

    def get_market_concept_min_east(self, index_code='BK0612'):
        """
        获取概念行情当日分时
        https://quote.eastmoney.com/bk/90.BK0612.html#fullScreenChart
        :param index_code: 概念指数代码
        :return 时间，现价，成交额（元），均价，成交量（股） 涨跌额，涨跌幅
        'index_code', 'trade_time', 'price', 'change', 'change_pct', 'volume', 'avg_price', 'amount'
        """
        url = f"https://push2his.eastmoney.com/api/qt/stock/trends2/get?" \
              f"fields2=f51,f52,f53,f54,f55,f56,f57,f58&secid=90.{index_code}&" \
              f"ndays=1&iscr=0&fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13"
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
        result_df = pd.DataFrame(data=data, columns=self.__MARKET_CONCEPT_MIN_COLUMNS)

        # 清洗数据
        result_df[['open', 'high', 'low', 'close', 'volume', 'amount', 'avg_price']] = \
            result_df[['open', 'high', 'low', 'close', 'volume', 'amount', 'avg_price']].astype(float)
        result_df['trade_time'] = pd.to_datetime(result_df['trade_date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        result_df['change'] = result_df['close'] - pre_price
        result_df['change_pct'] = result_df['change'] / pre_price * 100
        result_df = result_df.round(2)
        return result_df

    def get_market_concept_current_east(self, index_code: str = 'BK0900', k_type: int = 1):
        """
        https://push2.eastmoney.com/api/qt/stock/get?secid=90.BK0612&fields=f57,f58,f106,f59,f43,f46,f60,f44,f45,f47,f48,f49,f113,f114,f115,f117,f85,f50,f119,f120,f121,f122,f135,f136,f137,f138,f139,f140,f141,f142,f143,f144,f145,f146,f147,f148,f149
        :param index_code: 东方财富指数代码
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :return: k线行情数据 [概念代码,交易时间，交易日期，开，高，低，当前价格,成交量，成交额]
        """
        url = f"https://push2.eastmoney.com/api/qt/stock/get?secid=90.{index_code}&" \
              f"fields=f57,f58,f106,f59,f43,f46,f60,f44,f45,f47,f48,f49,f113,f114,f115,f117,f85,f50,f119,f120," \
              f"f121,f122,f135,f136,f137,f138,f139,f140,f141,f142,f143,f144,f145,f146,f147,f148,f149"
        res_json = requests.request('get', url, headers={}, proxies={}).json()
        # 解析数据
        j = res_json['data']
        if not j:
            return pd.DataFrame(data=[], columns=self.__MARKET_CONCEPT_CURRENT_COLUMNS)
        code = j['f57']
        if code != index_code:
            return pd.DataFrame(data=[], columns=self.__MARKET_CONCEPT_CURRENT_COLUMNS)
        pre_close = j['f60']
        data = [{'open': j['f46'], 'high': j['f44'], 'low': j['f45'], 'price': j['f43'], 'volume': j['f47'],
                 'amount': j['f48'], 'index_code': index_code}]
        result_df = pd.DataFrame(data=data, columns=self.__MARKET_CONCEPT_CURRENT_COLUMNS)

        # 清洗数据
        result_df[['open', 'high', 'low', 'price', 'volume', 'amount']] = \
            result_df[['open', 'high', 'low', 'price', 'volume', 'amount']].astype(float)
        result_df['change'] = result_df['price'] - pre_close
        result_df['change_pct'] = result_df['change'] / pre_close * 100
        result_df = result_df.round(2)
        return result_df


if __name__ == '__main__':
    print(ConceptMarketEase().get_market_concept_east(index_code='BK0612'))
    print(ConceptMarketEase().get_market_concept_min_east(index_code='BK0612'))
    print(ConceptMarketEase().get_market_concept_current_east(index_code='BK0900'))
