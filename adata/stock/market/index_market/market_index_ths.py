# -*- coding: utf-8 -*-
"""
@summary: 股票指数 行情
@author: 1nchaos
@date: 2023/06/01 16:17
"""
import copy
import json

import numpy as np
import pandas as pd

from adata.common.base.base_ths import BaseThs
from adata.common.exception.exception_msg import *
from adata.common.headers import ths_headers
from adata.stock.cache.index_code_rel_ths import rel


class StockMarketIndexThs(BaseThs):
    """
    股票指数 行情
    """
    __MARKET_INDEX_COLUMNS = ['index_code', 'trade_time', 'trade_date', 'open', 'high', 'low', 'close', 'volume',
                              'amount', 'change', 'change_pct']
    __MARKET_INDEX_MIN_COLUMNS = ['index_code', 'trade_time', 'trade_date', 'price', 'avg_price',
                                  'volume', 'amount', 'change', 'change_pct']
    __MARKET_INDEX_CURRENT_COLUMNS = ['index_code', 'trade_time', 'trade_date', 'open', 'high', 'low', 'price',
                                      'volume', 'amount']

    def __init__(self) -> None:
        super().__init__()

    def get_market_index(self, index_code: str = '000001', start_date='2020-01-01', k_type: int = 1):
        """
        获取指数行情数据
        http://d.10jqka.com.cn/v4/line/zs_1A0001/01/2022.js
        :param start_date: 开始时间
        :param index_code: 指数代码
        :param k_type:  k线类型：1.日；2.周；3.月 默认：1 日k
        :return: ['trade_date', 'open', 'high', 'low', 'close', 'volume', 'amount']
        """
        # 0. 时间范围处理
        years = self._get_years_by_start_date(start_date)
        concept_code = rel[index_code] if index_code in rel.keys() else index_code
        data = []
        for year in years:
            # 1.接口 url
            api_url = f"http://d.10jqka.com.cn/v4/line/zs_{concept_code}/{k_type - 1}1/{year}.js"
            # 同花顺可能ip限制，降低请求次数
            text = self._get_text(api_url, concept_code)
            if THS_IP_LIMIT_RES in text:
                return Exception(THS_IP_LIMIT_MSG)
            # 为空继续
            if not text:
                continue
            # 2. 解析数据
            result_text = text[text.index('{'):-1]
            data_list = json.loads(result_text)['data'].split(';')
            for d in data_list:
                data.append(str(d).split(',')[0:7])
        # 3. 数据etl
        result_df = pd.DataFrame(data=data, columns=['trade_date', 'open', 'high', 'low', 'close', 'volume', 'amount'])
        result_df.drop_duplicates(subset=['trade_date'], inplace=True)
        result_df = result_df.sort_values(by='trade_date', ascending=True)
        # 去重，日期升序
        result_df['index_code'] = index_code
        result_df['trade_time'] = pd.to_datetime(result_df['trade_date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        result_df['trade_date'] = pd.to_datetime(result_df['trade_date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
        result_df['close'] = result_df['close'].astype(float)
        result_df['change'] = result_df['close'] - result_df['close'].shift(1)
        result_df['change_pct'] = result_df['change'] / result_df['close'].shift(1) * 100
        result_df = result_df.round(2)
        result_df['close'] = result_df['close'].apply(lambda x: format(x, '.2f'))
        result_df.replace('--', None, inplace=True)
        result_df.replace('', None, inplace=True)
        result_df.replace(np.nan, None, inplace=True)
        # 4. 筛选时间范围
        if start_date:
            result_df = result_df[result_df['trade_date'] >= start_date]
        return result_df[self.__MARKET_INDEX_COLUMNS]

    def get_market_index_min(self, index_code='000001'):
        """
        获取概念行情当日分时
        web： http://d.10jqka.com.cn/v4/time/zs_1A0001/last.js
        0930,958.901,74456973,36.807,2022925;  "pre": "960.374",
        :param index_code: 概念指数代码
        :return 时间，现价，成交额（元），均价，成交量（股） 涨跌额，涨跌幅
        ['index_code', 'trade_time', 'price', 'change', 'change_pct', 'volume', 'avg_price', 'amount']
        """
        # 0. 指数代码转换
        concept_code = rel[index_code] if index_code in rel.keys() else index_code
        # 1.接口 url
        api_url = f"http://d.10jqka.com.cn/v4/time/zs_{concept_code}/last.js"
        text = self._get_text(api_url, concept_code)
        if THS_IP_LIMIT_RES in text:
            return Exception(THS_IP_LIMIT_MSG)
        if not text:
            return pd.DataFrame(data=[], columns=self.__MARKET_INDEX_MIN_COLUMNS)
        # 2. 解析数据
        result_json = json.loads(text[text.index('{'):-1])[f"zs_{concept_code}"]
        pre_price = result_json['pre']
        trade_date = result_json['date']
        data_list = result_json['data'].split(';')
        data = []
        for d in data_list:
            data.append(str(d).split(','))
        # 3. 封装数据
        result_df = pd.DataFrame(data=data, columns=['trade_time', 'price', 'amount', 'avg_price', 'volume'])
        result_df['index_code'] = index_code
        result_df['trade_time'] = trade_date + result_df['trade_time']
        result_df['trade_date'] = pd.to_datetime(trade_date, format='%Y%m%d').strftime('%Y-%m-%d')
        result_df['trade_time'] = pd.to_datetime(result_df['trade_time'], format='%Y%m%d%H%M').dt.strftime(
            '%Y-%m-%d %H:%M:%S')
        result_df['price'] = result_df['price']
        result_df['change'] = result_df['price'].astype(float) - float(pre_price)
        result_df['change_pct'] = result_df['change'] / float(pre_price) * 100

        result_df['change'] = result_df['change'].apply(lambda x: format(x, '.2f'))
        result_df['change_pct'] = result_df['change_pct'].apply(lambda x: format(x, '.2f'))
        result_df.replace('--', None, inplace=True)
        result_df.replace('', None, inplace=True)
        result_df.replace(np.nan, None, inplace=True)
        return result_df[self.__MARKET_INDEX_MIN_COLUMNS]

    def get_market_index_current(self, index_code: str = '000001', k_type: int = 1):
        """
        获取当前的指数行情
        web: http://q.10jqka.com.cn/gn/
        pc: http://d.10jqka.com.cn/v4/line/zs_1A0001/21/today.js
        quotebridge_v4_line_zs_1A0001_21_today({"zs_1A0001":{"1":"20230602","7":"3196.15","8":"3233.99","9":"3189.52",
        "11":"3230.07","13":60699786000,"19":"778489410000.00","74":"","1968584":"1.428","66":null,"open":1,"dt":"1755",
        "name":"\u4e0a\u8bc1\u6307\u6570","marketType":""}})
        :param index_code: 指数代码
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :return: [指数代码,交易时间，交易日期，开，高，低，当前价格,成交量，成交额]
        ['trade_time', 'trade_date', 'open', 'high', 'low', 'price', 'volume', 'amount']
        """
        # 0. 指数代码转换
        concept_code = rel[index_code] if index_code in rel.keys() else index_code
        # 1.接口 url
        api_url = f"http://d.10jqka.com.cn/v4/line/zs_{concept_code}/{k_type - 1}1/today.js"
        headers = copy.deepcopy(ths_headers.text_headers)
        headers['Host'] = 'd.10jqka.com.cn'
        # 同花顺可能ip限制，降低请求次数
        text = self._get_text(api_url, concept_code)
        if THS_IP_LIMIT_RES in text:
            return Exception(THS_IP_LIMIT_MSG)
        result_text = text[text.index('{'):-1]
        data_list = [json.loads(result_text)[f"zs_{concept_code}"]]
        rename = {'1': 'trade_date', '7': 'open', '8': 'high', '9': 'low', '11': 'price', '13': 'volume',
                  '19': 'amount', 'open': 'status'}
        result_df = pd.DataFrame(data=data_list).rename(columns=rename)
        result_df['trade_time'] = result_df['trade_date'] + result_df['dt']
        result_df['trade_time'] = pd.to_datetime(result_df['trade_time'], format='%Y%m%d%H%M').dt.strftime(
            '%Y-%m-%d %H:%M:%S')
        columns = ['trade_time', 'trade_date', 'open', 'high', 'low', 'price', 'volume', 'amount']
        result_df = result_df[columns]
        result_df['index_code'] = index_code
        result_df['trade_date'] = pd.to_datetime(result_df['trade_date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
        return result_df[self.__MARKET_INDEX_CURRENT_COLUMNS]


if __name__ == '__main__':
    print(StockMarketIndexThs().get_market_index(index_code='000001', start_date='2022-12-01'))
    print(StockMarketIndexThs().get_market_index_min(index_code='000001'))
    print(StockMarketIndexThs().get_market_index_current(index_code='000001'))
