# -*- coding: utf-8 -*-
"""
@summary: ETF 行情
https://d.10jqka.com.cn/v6/line/hs_512880/11/last360.js

@author: 1nchaos
@date: 2023/3/30 16:17
"""
import json

import numpy as np
import pandas as pd

from adata.common.base.base_ths import BaseThs
from adata.common.exception.exception_msg import *
from adata.fund.market.etf_market_template import ETFMarketTemplate


class ETFMarketThs(BaseThs, ETFMarketTemplate):
    """
    股票概念 行情
    """

    def get_market_etf_ths(self, fund_code: str = '512880', k_type: int = 1, start_date='', end_date=''):
        """
        获取同花顺的ETF的行情
        app: https://d.10jqka.com.cn/v6/line/hs_512880/01/last36000.js
        00 日k不复权；01日k前复权；02日k后复权；11周k前复权；21月k前复权
        :param start_date: 开始时间
        :param end_date: 结束时间
        :param fund_code: ETF代码
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :return: k线行情数据 [日期，开，高，低，收,成交量，成交额]
        ;20230419,958.901,981.118,958.449,961.107,521143220,20442229000.000
        成交量：股 820953530  821万手
        成交额：元 16959251000.000 169.6亿
        """
        # 0.参数校验
        # 1.接口 url
        api_url = f"http://d.10jqka.com.cn/v6/line/hs_{fund_code}/{k_type - 1}1/last36000.js"
        # 同花顺可能ip限制，降低请求次数
        text = self._get_text(api_url, fund_code)
        if THS_IP_LIMIT_RES in text:
            return Exception(THS_IP_LIMIT_MSG)
        result_text = text[text.index('{'):-1]
        data_list = json.loads(result_text)['data'].split(';')
        data = []
        for d in data_list:
            data.append(str(d).split(',')[0:7])
        result_df = pd.DataFrame(data=data, columns=['trade_date', 'open', 'high', 'low', 'close', 'volume', 'amount'])
        result_df['index_code'] = fund_code
        result_df['trade_time'] = pd.to_datetime(result_df['trade_date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        result_df['trade_date'] = pd.to_datetime(result_df['trade_date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
        result_df['close'] = result_df['close'].astype(float)
        result_df['change'] = result_df['close'] - result_df['close'].shift(1)
        result_df['change_pct'] = result_df['change'] / result_df['close'].shift(1) * 100

        # 3. 清洗数据
        result_df = result_df.round(3)
        result_df['close'] = result_df['close'].apply(lambda x: format(x, '.3f'))
        result_df.replace('--', None, inplace=True)
        result_df.replace('', None, inplace=True)
        result_df.replace(np.nan, None, inplace=True)
        # 4. 时间范围
        start_date = start_date if start_date else '1990-01-01'
        end_date = end_date if end_date else '2099-01-01'
        result_df = result_df[(result_df['trade_date'] >= start_date) & (result_df['trade_date'] <= end_date)]
        return result_df[self._MARKET_COLUMNS]

    def get_market_etf_min_ths(self, fund_code='512880'):
        """
        获取etf行情当日分时
        web： https://d.10jqka.com.cn/v6/time/hs_512880/last.js
        0930,958.901,74456973,36.807,2022925;  "pre": "960.374",
        :param fund_code: ETF代码
        :return 时间，现价，成交额（元），均价，成交量（股） 涨跌额，涨跌幅
        'index_code', 'trade_time', 'price', 'change', 'change_pct', 'volume', 'pre_close', 'amount'
        """
        # 0.参数校验
        # 1.接口 url
        api_url = f"http://d.10jqka.com.cn/v6/time/hs_{fund_code}/last.js"
        text = self._get_text(api_url, fund_code)
        if THS_IP_LIMIT_RES in text:
            return Exception(THS_IP_LIMIT_MSG)
        # 2. 解析数据
        result_json = json.loads(text[text.index('{'):-1])[f"hs_{fund_code}"]
        pre_price = result_json['pre']
        trade_date = result_json['date']
        data_list = result_json['data'].split(';')
        data = []
        for d in data_list:
            data.append(str(d).split(','))
        # 3. 封装数据
        result_df = pd.DataFrame(data=data, columns=['trade_time', 'price', 'amount', 'avg_price', 'volume'])
        result_df['index_code'] = fund_code
        result_df['trade_time'] = trade_date + result_df['trade_time']
        result_df['trade_date'] = pd.to_datetime(trade_date, format='%Y%m%d').strftime('%Y-%m-%d')
        result_df['trade_time'] = pd.to_datetime(result_df['trade_time'], format='%Y%m%d%H%M').dt.strftime(
            '%Y-%m-%d %H:%M:%S')
        result_df['price'] = result_df['price']
        result_df['change'] = result_df['price'].astype(float) - float(pre_price)
        result_df['change_pct'] = result_df['change'] / float(pre_price) * 100
        result_df.replace('--', None, inplace=True)
        result_df.replace('', None, inplace=True)
        result_df.replace(np.nan, None, inplace=True)
        return result_df[self._MARKET_ETF_MIN_COLUMNS]

    def get_market_etf_current_ths(self, fund_code: str = '512880', k_type: int = 1):
        """
        获取同花顺当前的概念行情
        web: https://d.10jqka.com.cn/v6/line/hs_512880/01/today.js
        quotebridge_v6_line_hs_512880_01_today({
        "hs_512880": { "1": "20240417", "7": "0.810", "8": "0.827", "9": "0.806","11": "0.825", "13": 1336243640,
        "19": "1092886150.000", "74": "","1968584": "3.727","66": "","open": 1,"dt": "1751","name": "\u8bc1\u5238ETF",
        "marketType": "" }})

        :param fund_code: ETF代码
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :return: k线行情数据 [ETF代码,交易时间，交易日期，开，高，低，当前价格,成交量，成交额]
        ;20230419,958.901,981.118,958.449,961.107,521143220,20442229000.000,存储芯片
        k:   1,      7,      8,       9,      11,      13,         19,        name
        成交量：股 820953530  821万手
        成交额：元 16959251000.000 169.6亿
        """
        # 0.参数校验
        # 1.接口 url
        api_url = f"http://d.10jqka.com.cn/v6/line/hs_{fund_code}/{k_type - 1}1/today.js"
        # 同花顺可能ip限制，降低请求次数
        text = self._get_text(api_url, fund_code)
        if THS_IP_LIMIT_RES in text:
            return Exception(THS_IP_LIMIT_MSG)
        result_text = text[text.index('{'):-1]
        data_list = [json.loads(result_text)[f"hs_{fund_code}"]]
        rename = {'1': 'trade_date', '7': 'open', '8': 'high', '9': 'low', '11': 'price', '13': 'volume',
                  '19': 'amount', 'open': 'status'}
        result_df = pd.DataFrame(data=data_list).rename(columns=rename)
        result_df['trade_time'] = result_df['trade_date'] + result_df['dt']
        result_df['trade_time'] = pd.to_datetime(result_df['trade_time'], format='%Y%m%d%H%M').dt.strftime(
            '%Y-%m-%d %H:%M:%S')
        columns = ['trade_time', 'trade_date', 'open', 'high', 'low', 'price', 'volume', 'amount']
        result_df = result_df[columns]
        result_df['index_code'] = fund_code
        result_df['trade_date'] = pd.to_datetime(result_df['trade_date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
        result_df['change'] = None
        result_df['change_pct'] = None
        return result_df[self._MARKET_ETF_CURRENT_COLUMNS]


if __name__ == '__main__':
    print(ETFMarketThs().get_market_etf_ths(fund_code='512880', start_date='2024-01-01'))
    print(ETFMarketThs().get_market_etf_ths(fund_code='159841', start_date='2024-01-01'))
    print(ETFMarketThs().get_market_etf_min_ths(fund_code='512880'))
    print(ETFMarketThs().get_market_etf_min_ths(fund_code='159841'))
    print(ETFMarketThs().get_market_etf_current_ths(fund_code='512880'))
    print(ETFMarketThs().get_market_etf_current_ths(fund_code='513800'))
