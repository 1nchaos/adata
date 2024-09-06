# -*- coding: utf-8 -*-
"""
@desc: 股票代码，上市日期等信息
深交所
http://www.szse.cn/market/product/stock/list/index.html
上海交易所
http://www.sse.com.cn/assortment/stock/list/share/
北交所
https://www.bse.cn/nq/listedcompany.html

东方财富：新股列表可做最新的补充
https://data.eastmoney.com/xg/xg/

@author: 1nchaos
@time: 2023/3/28
@log: change log
"""
import time

import numpy as np
import pandas as pd

from adata.common import requests
from adata.common.exception.handler import handler_null
from adata.common.headers import baidu_headers
from adata.common.utils.code_utils import get_exchange_by_stock_code
from adata.stock.cache import get_code_csv_path


class StockCode(object):
    """
    股票代码
    """
    __CODE_COLUMNS = ['stock_code', 'short_name', 'exchange', 'list_date']

    def __init__(self) -> None:
        super().__init__()

    def all_code(self):
        """
        获取所有股票的代码
        :return: 所有股票的代码信息：  ['stock_code', 'short_name', 'exchange', 'list_date']
        """
        # 拼接股票上市日期
        code = pd.read_csv(get_code_csv_path())[['stock_code', 'list_date2']]
        # 请求数据：优先东方财富，其次百度
        res_df = self.__market_rank_east()
        if res_df.empty:
            res_df = self.__market_rank_baidu()
        east = self.__new_sub_east()
        if not east.empty:
            res_df = pd.concat([east, res_df], axis=0, ignore_index=True)
            res_df = res_df.drop_duplicates(subset=['stock_code'], keep='first')
        res_df['stock_code'] = res_df['stock_code'].astype(str)
        code['stock_code'] = code['stock_code'].astype(str).str.zfill(6)
        df = pd.merge(res_df, code, on='stock_code', how='left')
        df['list_date'] = df['list_date'].fillna(df['list_date2'])
        df['list_date'] = pd.to_datetime(df['list_date'], errors='coerce').dt.date
        df['list_date'] = df['list_date'].where(df['list_date'].notnull(), np.nan)
        df['short_name'] = df['short_name'].str.replace(' ', '')
        return df.sort_values('stock_code').reset_index(drop=True)[self.__CODE_COLUMNS]

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
                res = requests.request(url=api_url, headers=baidu_headers.json_headers, proxies={})
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
        df = pd.DataFrame(data=data)[['code', 'name', 'exchange']].rename(columns=rename)
        df['list_date'] = np.nan
        return df[self.__CODE_COLUMNS]

    @handler_null
    def __new_sub_east(self):
        """
        东方财富新股申购列表
        https://data.eastmoney.com/xg/xg/default.html
        https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=APPLY_DATE,SECURITY_CODE&sortTypes=-1,-1&pageSize=50&pageNumber=1&reportName=RPTA_APP_IPOAPPLY&columns=SECURITY_CODE,SECURITY_NAME&quoteType=0&filter=(APPLY_DATE>'2010-01-01')&source=WEB&client=WEB
        """
        data = []
        for i in range(100):
            url = f"https://datacenter-web.eastmoney.com/api/data/v1/get?" \
                  f"sortColumns=APPLY_DATE,SECURITY_CODE&sortTypes=-1,-1&pageSize=50&pageNumber={i + 1}&" \
                  f"reportName=RPTA_APP_IPOAPPLY&columns=SECURITY_CODE,SECURITY_NAME,TRADE_MARKET,LISTING_DATE&quoteType=0&" \
                  f"filter=(APPLY_DATE>'2010-01-01')&source=WEB&client=WEB"
            res_json = requests.request('get', url, headers={}, proxies={}).json()
            res_data = res_json['result']['data']
            for _ in res_data:
                exchange = str(_['TRADE_MARKET'])
                if exchange.startswith('上海'):
                    exchange = 'SH'
                elif exchange.startswith('深圳'):
                    exchange = 'SZ'
                elif exchange.startswith('北京'):
                    exchange = 'BJ'
                if _['LISTING_DATE']:
                    data.append({'stock_code': _['SECURITY_CODE'], 'short_name': _['SECURITY_NAME'],
                                 'exchange': exchange, 'list_date': _['LISTING_DATE']})
            # if pd.to_datetime(data[-1]['list_date']) < pd.to_datetime('2023-10-01'):
            if pd.to_datetime(data[-1]['list_date']) < pd.to_datetime('2020-01-01'):
                break
        result_df = pd.DataFrame(data=data, columns=self.__CODE_COLUMNS)
        result_df['list_date'] = pd.to_datetime(result_df['list_date']).dt.date
        return result_df

    @handler_null
    def __market_rank_east(self):
        """
        东方财富新股申购列表
        https://quote.eastmoney.com/center/gridlist.html
        """
        url = "https://82.push2.eastmoney.com/api/qt/clist/get"
        params = {
            "pn": "1", "pz": "50000",
            "po": "1", "np": "1",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": "2", "invt": "2", "fid": "f3",
            "fs": "m:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048",
            "fields": "f12,f14",
            "_": "1623833739532",
        }
        # 请求数据
        r = requests.request(url, timeout=15, params=params)
        data_json = r.json()
        if not data_json["data"]["diff"]:
            return pd.DataFrame()
        df = pd.DataFrame(data=data_json["data"]["diff"])
        df.columns = ['stock_code', 'short_name']
        # 数据etl
        df['exchange'] = df['stock_code'].apply(lambda x: get_exchange_by_stock_code(x))
        df['list_date'] = np.nan
        df.reset_index(inplace=True)
        return df[self.__CODE_COLUMNS]


if __name__ == '__main__':
    print(StockCode().all_code())
