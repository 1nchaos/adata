# -*- coding: utf-8 -*-
"""
@desc:
融资融券数据
同花顺
http://data.10jqka.com.cn/market/rzrq/
http://data.10jqka.com.cn/market/rzrq/board/getRzrqPage/page/2/ajax/1/
东方财富
https://data.eastmoney.com/rzrq/total.html
https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPTA_RZRQ_LSHJ&columns=ALL&source=WEB&sortColumns=dim_date&sortTypes=-1&pageNumber=2&pageSize=50&filter=&pageNo=2&p=2&pageNum=2&_=1690176931022

@author: 1nchaos
@time: 2023/7/24
@log: change log
"""
from datetime import datetime

import pandas as pd

from adata.common import requests
from adata.common.headers import east_headers


class SecuritiesMargin(object):
    __SECURITIES_MARGIN_COLUMN = ['trade_date', 'rzye', 'rqye', 'rzrqye', 'rzrqyecz']

    def __init__(self) -> None:
        super().__init__()

    def securities_margin(self, start_date=None):
        """
        查询开始时间到现在的融资融券余额数据，默认：查询最近一年的数据
        :return:  ['trade_date', 'rzye', 'rqye', 'rzrqye', 'rzrqyecz']
        trade_date: 交易日
        rzye： 融资余额（元）
        rqye： 融券余额（元）
        rzrqye： 融资融券余额（元）
        rzrqyecz： 融资融券余额差值（元）
        """
        return self.__securities_margin_east(start_date=start_date)

    def __securities_margin_east(self, start_date=None):
        """
        https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPTA_RZRQ_LSHJ&columns=ALL&source=WEB&sortColumns=dim_date&sortTypes=-1&pageNumber=1&pageSize=250&_=1690176931022
        :param start_date: 开始时间
        :return:
        """
        # 1. url拼接页码等参数
        data = []
        total_pages = 1
        curr_page = 1
        page_size = 250
        start_date_str = start_date
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        while curr_page <= total_pages:
            api_url = f"https://datacenter-web.eastmoney.com/api/data/v1/get?" \
                      f"reportName=RPTA_RZRQ_LSHJ&columns=ALL&source=WEB&sortColumns=dim_date&sortTypes=-1&" \
                      f"pageNumber={curr_page}&pageSize={page_size}&_=1690176931022"

            res = requests.request(method='get', url=api_url, headers=east_headers.json_headers, proxies={})
            # 2. 判断请求是否成功
            if res.status_code != 200:
                continue
            res_json = res.json()
            if not res_json['success']:
                continue
            if curr_page == 1:
                total_pages = res_json['result']['pages']
            res_json = res_json['result']['data']
            # 2.1 日期范围判断
            data.extend(res_json)
            if not start_date:
                break
            if start_date:
                date_min = datetime.strptime(res_json[-1]['DIM_DATE'], '%Y-%m-%d %H:%M:%S')
                if start_date >= date_min:
                    break
            curr_page += 1

        # 3. 解析数据
        result_df = pd.DataFrame(data=data)
        rename_columns = {'RZYE': 'rzye', 'RQYE': 'rqye', 'RZRQYE': 'rzrqye', 'RZRQYECZ': 'rzrqyecz',
                          'DIM_DATE': 'trade_date'}
        result_df = result_df.rename(columns=rename_columns)[self.__SECURITIES_MARGIN_COLUMN]

        # 4. 数据清洗
        result_df['trade_date'] = pd.to_datetime(result_df['trade_date']).dt.strftime('%Y-%m-%d')
        result_df = result_df[result_df['trade_date'] > start_date_str]
        return result_df


if __name__ == '__main__':
    print(SecuritiesMargin().securities_margin('2022-01-01'))
