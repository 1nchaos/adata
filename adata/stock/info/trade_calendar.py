# -*- coding: utf-8 -*-
"""
@desc: 交易日历
@author: 1nchaos
@time: 2023/3/28
@log: change log
"""
import datetime

import pandas as pd
from tqdm import tqdm

from adata.common import requests
from adata.stock.cache.calendar import years, get_csv_path


class TradeCalendar(object):
    """
    交易日历
    """
    __COLUMNS = ['trade_date', 'trade_status', 'day_week']

    def __init__(self) -> None:
        super().__init__()

    def trade_calendar(self, year=None):
        """
        获取股票交易日历
        :return: 交易日历信息：
        trade_date: 交易日;
        day_week: 一周的第几天，从星期日开始;
        trade_status: 交易状态:1，交易日；0，非交易日
        """
        # 先获取缓存数据
        if not year:
            year = datetime.datetime.now().year
        if year in years:
            return pd.read_csv(get_csv_path(year), header=0)
        return self.__calendar_szse(year=year)

    def __calendar_szse(self, year=None):
        """
        获取深交所交易日历
        web_url :http://www.szse.cn/api/report/exchange/onepersistenthour/monthList?month=2023-1
        :param year: 年份：'2023'
        :return: ['trade_date','day_week','trade_status']
        """
        # 1. url，拼接月份
        data = []
        for i in tqdm(range(12)):
            api_url = f"http://www.szse.cn/api/report/exchange/onepersistenthour/monthList?month={year}-{i + 1}"
            res = requests.request(method='get', url=api_url, headers={}, proxies={})
            # 2. 判断请求是否成功
            if res.status_code != 200:
                continue
            res_json = res.json()
            # 3. 解析数据
            result = res_json['data']
            # 结果为空跳出循环
            if not result:
                break
            data.extend(result)
        # 4. 封装数据
        rename = {'jyrq': 'trade_date', 'jybz': 'trade_status', 'zrxh': 'day_week'}
        if not data:
            return pd.DataFrame(data=data, columns=self.__COLUMNS)
        return pd.DataFrame(data=data).rename(columns=rename)[self.__COLUMNS]


if __name__ == '__main__':
    print(TradeCalendar().trade_calendar(year=2004))
    print(TradeCalendar().trade_calendar())
