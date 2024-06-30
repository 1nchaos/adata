# -*- coding: utf-8 -*-
"""
@desc: 股票分红信息
数据来源：1. 百度

@author: 1nchaos
@time: 2023/3/29
@log: change log
"""

import pandas as pd
import numpy as np

from adata.common.headers import baidu_headers
from adata.common.utils import requests


class StockDividend(object):
    """
    股票分红
    """

    def __init__(self) -> None:
        super().__init__()

    def get_dividend(self, stock_code='000001'):
        """
        获取当个股票的分红信息
        :param stock_code: 股票代码
        :return: 股票分红信息
        """
        return self.__dividend_baidu(stock_code)

    def __dividend_baidu(self, stock_code):
        """
        获取百度的股票分红数据：公告日；分红方案；除权除息日
        web： https://gushitong.baidu.com/stock/ab-300033
        url： https://gushitong.baidu.com/opendata?openapi=1&dspName=iphone&tn=tangram&
        client=app&query=300033&code=300033&word=300033&resource_id=5429&ma_ver=4&finClientType=pc
        :param stock_code: 6位股票代码
        :return: 股票分红信息
        """
        columns = ['report_date', 'dividend_plan', 'ex_dividend_date']
        null_df = pd.DataFrame(data=[], columns=columns)
        # 1.请求接口 url
        api_url = f"https://gushitong.baidu.com/opendata?openapi=1&dspName=iphone&tn=tangram&client=app&" \
                  f"query={stock_code}&code={stock_code}&word={stock_code}&resource_id=5429&ma_ver=4&finClientType=pc"
        res = requests.request('get', api_url, headers=baidu_headers.text_headers)

        # 2. 判断结果是否正确
        if len(res.text) < 1 or res.status_code != 200:
            return pd.DataFrame()
        res_json = res.json()
        if res_json['ResultCode'] != '0':
            return null_df
        # 3.解析数据
        # 3.1 空数据时返回为空
        result = res_json['Result']
        if not result:
            return null_df

        # 3.2 正常解析数据 basicInfo,shareholderEquity,organRating,executiveInfo,bonusTransfer
        try:
            new_company = result[-1]['DisplayData']['resultData']['tplData']['result']['tabs'][-1]['content'][
                'newCompany']
            bonus_transfer = new_company['bonusTransfer']
            body = bonus_transfer['body']
        except KeyError:
            return null_df

        # 4. 封装数据
        result_df = pd.DataFrame(data=body, columns=['公告日', '分红方案', '除权除息日', '信息'])
        result_df['stock_code'] = stock_code
        rename_columns = {'公告日': 'report_date', '分红方案': 'dividend_plan', '除权除息日': 'ex_dividend_date'}
        result_df = result_df.rename(columns=rename_columns)
        # 5. 数据清洗
        result_df = result_df[result_df.dividend_plan != '利润不分配']
        result_df['ex_dividend_date'] = result_df['ex_dividend_date'].replace('--', np.nan)
        return result_df[['stock_code', 'report_date', 'dividend_plan', 'ex_dividend_date']]


if __name__ == '__main__':
    print(StockDividend().get_dividend(stock_code='600781'))
