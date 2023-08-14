# -*- coding: utf-8 -*-
"""
@desc: 股票代码
@author: 1nchaos
@time: 2023/3/28
@log: change log
"""
import time

import pandas as pd
import requests

from adata.common.exception.handler import handler_null
from adata.common.headers import baidu_headers


class StockCode(object):
    """
    股票代码
    """
    __CODE_COLUMNS = ['stock_code', 'short_name', 'exchange']

    def __init__(self) -> None:
        super().__init__()

    def all_code(self):
        """
        获取所有股票的代码 ,后续补充多数据源
        :return: 所有股票的代码信息： ['stock_code','short_name','exchange']
        """
        res_df = self.__market_rank_baidu()
        east = self.__new_sub_east()
        if not east.empty:
            res_df = pd.concat([east, res_df], axis=0, ignore_index=True)
            res_df = res_df.drop_duplicates(subset=['stock_code'], keep='first')
        return res_df.sort_values('stock_code').reset_index(drop=True)

    def __market_rank_baidu(self):
        """
        获取百度当前涨幅排名的代码
        web： https://gushitong.baidu.com/top/ab-increase-%E6%B6%A8%E5%B9%85%E6%A6%9C
        url：https://finance.pae.baidu.com/selfselect/getmarketrank?sort_type=1&sort_key=14&from_mid=1&pn=0&rn=200&group=pclist&type=ab&finClientType=pc
        其中：pn 起始数 rn 翻页数，最大200
        :return 代码列表：['stock_code','short_name','exchange']
        """
        # 1. 请求市场排名的 url
        api_url = f"https://finance.pae.baidu.com/selfselect/getmarketrank" \
                  f"?sort_type=1&sort_key=14&from_mid=1&group=pclist&type=ab&finClientType=pc"
        max_page_size = 200
        data = []

        # 2. 一直翻页请求数据，股票目前数据5000,50页一共1w只,后续增加了可以再加
        for page_no in range(49):
            api_url = f"{api_url}&pn={page_no * max_page_size}&rn={max_page_size}"
            try:
                res = requests.get(api_url, headers=baidu_headers.json_headers, proxies={})
                res_json = res.json()
                if res.status_code != 200 or res_json['ResultCode'] != '0':
                    continue
                # 3. 解析数据
                result = res_json['Result']['Result']
                # 结果为空跳出循环
                if not result:
                    break
                code_list = result[0]['DisplayData']['resultData']['tplData']['result']['rank']
                data.extend(code_list)
            except Exception as e:
                time.sleep(2)
                print(e)
                continue
        # 4. 封装数据
        rename = {'name': 'short_name', 'code': 'stock_code'}
        return pd.DataFrame(data=data)[['code', 'name', 'exchange']].rename(columns=rename)[self.__CODE_COLUMNS]

    @handler_null
    def __new_sub_east(self):
        """
        东方财富新股申购列表
        https://data.eastmoney.com/xg/xg/default.html
        https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=APPLY_DATE,SECURITY_CODE&sortTypes=-1,-1&pageSize=50&pageNumber=1&reportName=RPTA_APP_IPOAPPLY&columns=SECURITY_CODE,SECURITY_NAME&quoteType=0&filter=(APPLY_DATE>'2010-01-01')&source=WEB&client=WEB
        """
        url = f"https://datacenter-web.eastmoney.com/api/data/v1/get?" \
              f"sortColumns=APPLY_DATE,SECURITY_CODE&sortTypes=-1,-1&pageSize=50&pageNumber=1&" \
              f"reportName=RPTA_APP_IPOAPPLY&columns=SECURITY_CODE,SECURITY_NAME,TRADE_MARKET&quoteType=0&" \
              f"filter=(APPLY_DATE>'2010-01-01')&source=WEB&client=WEB"
        res_json = requests.request('get', url, headers={}, proxies={}).json()
        res_data = res_json['result']['data']
        data = []
        for _ in res_data:
            exchange = str(_['TRADE_MARKET'])
            if exchange.startswith('上海'):
                exchange = 'SH'
            elif exchange.startswith('深圳'):
                exchange = 'SZ'
            elif exchange.startswith('北京'):
                exchange = 'BJ'
            data.append({'stock_code': _['SECURITY_CODE'], 'short_name': _['SECURITY_NAME'], 'exchange': exchange})
        result_df = pd.DataFrame(data=data, columns=self.__CODE_COLUMNS)
        return result_df


if __name__ == '__main__':
    print(StockCode().all_code())
