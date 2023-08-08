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

from adata.common.headers import baidu_headers


class StockCode(object):
    """
    股票代码
    """

    def __init__(self) -> None:
        super().__init__()

    def all_code(self):
        """
        获取所有股票的代码 ,后续补充多数据源
        :return: 所有股票的代码信息： ['stock_code','short_name','exchange']
        """
        return self.__market_rank_baidu()

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
        return pd.DataFrame(data=data)[['code', 'name', 'exchange']].rename(columns=rename)


if __name__ == '__main__':
    print(StockCode().all_code())
