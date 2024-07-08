# -*- coding: utf-8 -*-
"""
@desc: 百度股市通
https://gushitong.baidu.com/

@author: 1nchaos
@time: 2023/06/19
@log: change log
"""

import time

import pandas as pd

from adata.common.headers import baidu_headers
from adata.common.utils import requests
from adata.stock.market.index_market.market_index_template import StockMarketIndexTemplate


class StockMarketIndexBaidu(StockMarketIndexTemplate):
    """
    百度股票行情
    """

    def __init__(self) -> None:
        super().__init__()

    def get_market_index(self, index_code: str = '000001', start_date='2020-01-01', k_type: int = 1):
        """
        获取百度的股票行情数据
        web： https://gushitong.baidu.com/stock/ab-000001
        "ma5均价","ma5成交量","ma10均价","ma10成交量","ma20均价","ma20成交量"
        :param index_code: 6位股票代码
        :param start_date: 开始时间
        :param k_type: k线类型：1.日；2.周；3.月
        # :param adjust_type: k线复权类型：0.不复权；1.前复权；2.后复权 默认：1 前复权 TODO
        :return: k线行情数据:"时间戳", "时间","开盘","收盘","成交量","最高","最低","成交额","涨跌额","涨跌幅","换手率","昨收"
        """
        # 1. 请求接口 url
        api_url = f" https://finance.pae.baidu.com/vapi/v1/getquotation?srcid=5353&all=1&pointType=string&" \
                  f"group=quotation_index_kline&query={index_code}&code={index_code}&market_type=ab&" \
                  f"newFormat=1&is_kc=0&ktype=day&finClientType=pc"

        res_json = None
        for i in range(3):
            res = requests.request('get', api_url, headers=baidu_headers.json_headers, proxies={})
            # 2. 校验请求结果数据
            res_json = res.json()
            if res_json['ResultCode'] == '0':
                break
            time.sleep(2)
        # 3.解析数据
        # 3.1 空数据时返回为空
        result = res_json['Result']
        if not result:
            return pd.DataFrame(data=[], columns=self._MARKET_INDEX_COLUMNS)

        # 3.2. 正常解析数据
        keys = res_json['Result']['newMarketData']['keys']
        market_data = res_json['Result']['newMarketData']['marketData']
        market_data_list = str(market_data).split(';')
        data = []
        for one in market_data_list:
            data.append(one.split(','))

        # 4. 封装数据
        rename_columns = {'turnoverratio': 'turnover_ratio', 'preClose': 'pre_close', 'range': 'change',
                          'ratio': 'change_pct', 'time': 'trade_time'}
        result_df = pd.DataFrame(data=data, columns=keys).rename(columns=rename_columns)[
            self._MARKET_INDEX_BASE_COLUMNS]
        if result_df.empty:
            return pd.DataFrame(data=[], columns=self._MARKET_INDEX_COLUMNS)
        result_df['index_code'] = index_code
        result_df['trade_date'] = result_df['trade_time']
        result_df['trade_time'] = pd.to_datetime(result_df['trade_time']).dt.strftime('%Y-%m-%d %H:%M:%S')
        # 5. 数据清洗，剔除成交量且成交额为0的异常数据
        result_df.replace('--', None, inplace=True)
        result_df.replace('', None, inplace=True)
        result_df['amount'] = result_df['amount'].astype(float)
        result_df['volume'] = result_df['volume'].astype(float)
        result_df = result_df[(result_df['amount'] > 0) | (result_df['volume'] > 0)]
        result_df['change'] = result_df['change'].str.replace('+', '').astype(float)
        result_df['change_pct'] = result_df['change_pct'].str.replace('+', '').astype(float)
        if start_date:
            result_df = result_df[result_df['trade_date'] >= start_date]
        return result_df


if __name__ == '__main__':
    print(StockMarketIndexBaidu().get_market_index(index_code='000001', start_date='2021-01-01', k_type=1))
