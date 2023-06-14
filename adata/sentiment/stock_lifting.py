# -*- coding: utf-8 -*-
"""
@desc: TODO
股票解禁：大概率大额解禁的票房风险较大，可以加入短线交易的因子数据
解禁数据：来源同花顺行情中心
http://data.10jqka.com.cn/market/xsjj/field/enddate/order/desc/ajax/1/free/1/
http://data.10jqka.com.cn/market/xsjj/field/enddate/order/desc/ajax/1/free/1/page/2/free/1/

@author: 1nchaos
@time: 2023/6/14
@log: change log
"""
import copy

import pandas as pd
from bs4 import BeautifulSoup

from adata.common import requests
from adata.common.headers import ths_headers


class StockLifting(object):
    __STOCK_LIFTING_COLUMN = ['stock_code', 'short_name', 'lift_date', 'volume', 'ratio', 'price', 'amount']

    def __init__(self) -> None:
        super().__init__()

    def stock_lifting_last_month(self):
        """
        查询最近一个月的股票解禁列表
        http://data.10jqka.com.cn/market/xsjj/field/enddate/order/desc/ajax/1/free/1/
        http://data.10jqka.com.cn/market/xsjj/field/enddate/order/desc/ajax/1/free/1/page/2/free/1/
        :return:  ['stock_code', 'short_name', 'lift_date', 'volume', 'ratio', 'price', 'amount']
        stock_code: 股票代码
        short_name： 股票简称
        lift_date： 解禁日期
        volume： 解禁股数（股）
        ratio： 占总股本比例（%）
        price： 最新股价（元）
        amount： 最新解禁金额（元）
        """
        # 1. url拼接页码等参数
        data = []
        total_pages = 1
        curr_page = 1
        while curr_page <= total_pages:
            api_url = f"http://data.10jqka.com.cn/market/xsjj/field/enddate/order/desc/ajax/1/free/1/"
            if curr_page > 1:
                api_url = api_url + f"page/{curr_page}/free/1/"
            headers = copy.deepcopy(ths_headers.text_headers)
            headers['Host'] = 'data.10jqka.com.cn'
            res = requests.request(method='get', url=api_url, headers=headers, proxies={})
            curr_page += 1
            # 2. 判断请求是否成功
            if res.status_code != 200:
                continue
            text = res.text
            if '解禁日期' in text or '解禁股' in text:
                break
            soup = BeautifulSoup(text, 'html.parser')
            # 3 .获取总的页数
            if total_pages == 1:
                page_info = soup.find('span', {'class': 'page_info'})
                if page_info:
                    total_pages = int(page_info.text.split("/")[1])
            # 4. 解析数据
            page_data = []
            for idx, tr in enumerate(soup.find_all('tr')):
                if idx != 0:
                    tds = tr.find_all('td')
                    page_data.append({'stock_code': tds[1].contents[0].text, 'short_name': tds[2].contents[0].text,
                                      'lift_date': tds[3].contents[0].text, 'volume': tds[4].contents[0].text,
                                      'ratio': tds[7].contents[0].text, 'price': tds[5].contents[0].text,
                                      'amount': tds[6].contents[0].text})
            data.extend(page_data)
        # 5. 封装数据
        if not data:
            return pd.DataFrame(data=data, columns=self.__STOCK_LIFTING_COLUMN)
        result_df = pd.DataFrame(data=data)
        data.clear()
        return result_df[self.__STOCK_LIFTING_COLUMN]


if __name__ == '__main__':
    print(StockLifting().stock_lifting_last_month())
