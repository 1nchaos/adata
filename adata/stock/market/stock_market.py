# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/3/29
@log: change log
"""

import time

import pandas as pd

from adata.common.headers import baidu_headers, sina_headers
from adata.common.utils import requests


class StockMarket(object):
    """
    股票行情 TODO 数据返回类型转换
    """
    __MARKET_COLUMNS = ['trade_time', 'open', 'close', 'volume', 'high', 'low', 'amount', 'change', 'change_pct',
                      'turnover_ratio', 'pre_close']
    __MARKET_MIN_COLUMNS = ['stock_code', 'trade_time', 'price', 'change', 'change_pct', 'volume', 'avg_price', 'amount']
    __MARKET_CURRENT_COLUMNS = ['stock_code', 'short_name', 'price', 'change', 'change_pct', 'volume', 'amount']

    def __init__(self) -> None:
        super().__init__()

    def get_market(self, stock_code: str = '000001', start_date='1990-01-01', k_type=1, adjust_type: int = 1):
        """
        获取单个股票的行情
        :param stock_code: 股票代码
        :param start_date: 开始时间
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :param adjust_type: k线复权类型：0.不复权；1.前复权；2.后复权 默认：1 前复权 （目前：只有前复权,作为股票交易已经可用）
        :return: k线行情数据
        """
        return self.__market_baidu(stock_code, start_date, k_type)

    def get_market_min(self, stock_code: str = '000001'):
        """
        获取单个股票的今日分时行情
        :param stock_code: 股票代码
        :return: 当日分钟行情数据
        """
        return self.__market_baidu_today_min(stock_code)

    def list_market_current(self, code_list=None):
        """
        获取多个股票最新行情信息
        :param code_list: 股票代码
        :return: 当前最新的行情价格信息
        """
        if code_list is None:
            return pd.DataFrame()
        return self.__market_sina_current(code_list=code_list)

    def __market_baidu(self, stock_code, start_date, k_type=1):
        """
        获取百度的股票行情数据
        web： https://gushitong.baidu.com/stock/ab-002926
        url：quotation_fiveday_ab 5日分时，quotation_kline_ab K线， quotation_minute_ab 当日分钟
        k线
        https://finance.pae.baidu.com/selfselect/getstockquotation?all=1&isIndex=false&isBk=false&isBlock=false&
        isFutures=false&isStock=true&newFormat=1&group=quotation_kline_ab&finClientType=pc&
        code=002926&start_time=2018-02-05 00:00:00&ktype=1
        分钟
        https://finance.pae.baidu.com/selfselect/getstockquotation?
        all=1&code=601318&isIndex=false&isBk=false&isBlock=false&isFutures=false&isStock=true&newFormat=1&
        group=quotation_minute_ab&finClientType=pc
        "ma5均价","ma5成交量","ma10均价","ma10成交量","ma20均价","ma20成交量"
        :param stock_code: 6位股票代码
        :param start_date: 开始时间
        :param k_type: k线类型：1.日；2.周；3.月
        # :param adjust_type: k线复权类型：0.不复权；1.前复权；2.后复权 默认：1 前复权 TODO
        :return: k线行情数据:"时间戳", "时间","开盘","收盘","成交量","最高","最低","成交额","涨跌额","涨跌幅","换手率","昨收"
        """
        # 1. 请求接口 url
        api_url = f"https://finance.pae.baidu.com/selfselect/getstockquotation?all=1&isIndex=false&isBk=false&" \
                  f"isBlock=false&isFutures=false&isStock=true&newFormat=1&group=quotation_kline_ab&finClientType=pc&" \
                  f"code={stock_code}&start_time={start_date} 00:00:00&ktype={k_type}"

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
            return pd.DataFrame(data=[], columns=self.__MARKET_COLUMNS)

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
        result_df = pd.DataFrame(data=data, columns=keys).rename(columns=rename_columns)[self.__MARKET_COLUMNS]
        result_df['stock_code'] = stock_code
        result_df['trade_date'] = result_df['trade_time']
        result_df['trade_time'] = pd.to_datetime(result_df['trade_time']).dt.strftime('%Y-%m-%d %H:%M:%S')
        result_df.replace('--', None, inplace=True)
        result_df.replace('', None, inplace=True)
        result_df['change'] = result_df['change'].str.replace('+', '', regex=True)
        result_df['change_pct'] = result_df['change_pct'].str.replace('+', '', regex=True)
        # 5. 数据清洗，剔除成交量为0的异常数据
        result_df['amount'] = result_df['amount'].astype(float)
        result_df = result_df[result_df['amount'] > 0]
        result_df.replace('--', None, inplace=True)
        result_df.replace('', None, inplace=True)
        result_df['change'] = result_df['change'].str.replace('+', '', regex=True).astype(float)
        result_df['change_pct'] = result_df['change_pct'].str.replace('+', '', regex=True).astype(float)
        return result_df

    def __market_baidu_today_min(self, stock_code):
        """
        获取百度的股票行情数据
        web： https://gushitong.baidu.com/stock/ab-002926
        url: https://finance.pae.baidu.com/selfselect/getstockquotation?
        all=1&code=601318&isIndex=false&isBk=false&isBlock=false&isFutures=false&isStock=true&newFormat=1
        &group=quotation_minute_ab&finClientType=pc
        time, price, ratio, increase, volume, avgPrice, amount, timeKey, datetime, oriAmount
        :param stock_code: 6位股票代码
        :return: k线行情数据:"时间","价格","涨跌率","涨幅","均价","成交量", "成交额"
        """
        # 1. 请求接口 url
        api_url = f"https://finance.pae.baidu.com/selfselect/getstockquotation?all=1&isIndex=false&isBk=false&" \
                  f"isBlock=false&isFutures=false&isStock=true&newFormat=1&group=quotation_minute_ab&" \
                  f"finClientType=pc&code={stock_code}"

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
            return pd.DataFrame(data=[], columns=self.__MARKET_MIN_COLUMNS)

        # 3.2. 正常解析数据
        market_data_list = res_json['Result']['priceinfo']

        # 4. 封装数据
        field = ['time', 'price', 'ratio', 'increase', 'volume', 'avgPrice', 'amount', 'timeKey', 'datetime',
                 'oriAmount']
        rename_columns = {'avgPrice': 'avg_price', 'oriAmount': 'ori_amount', 'ratio': 'change_pct',
                          'increase': 'change'}
        result_df = pd.DataFrame(data=market_data_list, columns=field).rename(columns=rename_columns)
        result_df['amount'] = result_df['ori_amount']
        result_df['stock_code'] = stock_code
        # 这里是分钟均价，数据存在四舍五入的情况
        result_df['volume'] = result_df['volume'].astype(int) * 100
        result_df['trade_time'] = pd.to_datetime(result_df['time'], unit='s', utc=True).dt.tz_convert(
            'Asia/Shanghai')
        result_df['trade_time'] = pd.to_datetime(result_df['trade_time']).dt.strftime("%Y-%m-%d %H:%M:%S")
        result_df['trade_date'] = result_df['trade_time'].str[:10]
        result_df['change'] = result_df['change'].str.replace('+', '', regex=True).astype(float)
        result_df['change_pct'] = result_df['change_pct'].str.replace('+', '', regex=True).astype(float)
        return result_df[self.__MARKET_MIN_COLUMNS]

    def __market_sina_current(self, code_list):
        """
        获取新浪的最新股票行情
        url : https://hq.sinajs.cn/list=s_sh600905,s_sz000725,s_sz000100,s_sh601919
        :param code_list:  代码列表
        :return: 最新行情数据：代码,简称,当前价格(元),涨跌额(元),涨跌幅(%),成交量(股),成交额(元)
        """
        # 0.进行参数拼接处理
        api_url = f"https://hq.sinajs.cn/list="
        for code in code_list:
            if code.startswith('0') or code.startswith('3'):
                api_url += 's_sz' + code + ','
            elif code.startswith('6') or code.startswith('9'):
                api_url += 's_sh' + code + ','
            elif code.startswith('4') or code.startswith('8'):
                api_url += 's_bj' + code + ','

        # 1.请求接口
        res = requests.request('get', api_url, headers=sina_headers.c_headers)

        # 2. 判断结果是否正确
        if len(res.text) < 1 or res.status_code != 200:
            return pd.DataFrame(data=[], columns=self.__MARKET_CURRENT_COLUMNS)
        # 3.解析数据

        # 正常解析数据 var hq_str_s_bj872925="平安银行,14.840,0.480,3.343,374847,5483780.180";
        data_list = res.text.split(';')
        data = []
        for data_str in data_list:
            if len(data_str) < 8:
                continue
            idx = data_str.index('=')
            code = [data_str[idx - 6:idx]]
            code.extend(data_str[idx + 2:-1].split(','))
            if len(code) == 7:
                data.append(code)

        # 4. 封装数据
        result_df = pd.DataFrame(data=data, columns=self.__MARKET_CURRENT_COLUMNS)
        # 北京的单位是股和万元
        mask = result_df['stock_code'].str.startswith(('0', '3', '6', '9'))
        result_df.loc[mask, 'volume'] = result_df['volume'].astype(int) * 100
        result_df.loc[mask, 'amount'] = result_df['amount'].astype(float) * 10000
        return result_df


if __name__ == '__main__':
    print(StockMarket().get_market(stock_code='000001', start_date='2021-01-01', k_type=1))
    # print(StockMarket().get_market_min(stock_code='000001'))
    # print(StockMarket().list_market_current(code_list=['000001', '600001', '000795', '872925']))
