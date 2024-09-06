# -*- coding: utf-8 -*-
"""
@desc: 债券代码
@author: 1nchaos
@time: 2023/5/31
@log: change log
"""
import copy

import pandas as pd
from adata.common import requests

from adata.common.headers import ths_headers


class BondCode(object):
    """
    债券代码
    """

    def __init__(self) -> None:
        super().__init__()

    def all_convert_code(self):
        """
        获取所有的可转换债券代码信息
        :return: 所有可转换债券的代码信息：
        ['bond_code','bond_name','stock_code','short_name','sub_date','issue_amount','listing_date',
        'expire_date','convert_price']
        """
        return self.__convert_code_ths()

    def __convert_code_ths(self):
        """
        获取同花顺可转换债券列表
        web： http://data.10jqka.com.cn/ipo/kzz/
        :return 可转债列表
        ['bond_code','bond_name','stock_code','short_name','sub_date','issue_amount','listing_date','expire_date',
        'convert_price']
        """
        COLUMNS = ['bond_code', 'bond_name', 'stock_code', 'short_name', 'sub_date', 'issue_amount', 'listing_date',
                   'expire_date', 'convert_price']
        # 1. 请求市场排名的 url
        api_url = f"https://data.10jqka.com.cn/ipo/kzz/"
        # 2. 设置请求头
        headers = copy.deepcopy(ths_headers.text_headers)
        headers['Host'] = 'data.10jqka.com.cn'
        headers['Referer'] = 'http://data.10jqka.com.cn/ipo/bond/'
        res = requests.request(url=api_url, headers=headers, proxies={})
        res_json = res.json()
        if res.status_code != 200 or res_json['status_msg'] != 'ok':
            return pd.DataFrame(data=[], columns=COLUMNS)
        # 3. 解析数据
        data = res_json['list']
        # 4. 封装数据
        rename = {'price': 'convert_price', 'issue_total': 'issue_amount', 'name': 'short_name', 'code': 'stock_code'}
        df = pd.DataFrame(data=data).rename(columns=rename)[COLUMNS]
        # 5. 数据清洗
        df['issue_amount'] = df['issue_amount'].astype(float) * 100000000
        return df


if __name__ == '__main__':
    print(BondCode().all_convert_code())
