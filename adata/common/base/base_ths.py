# -*- coding: utf-8 -*-
"""
@desc: 同花顺基础类
@author: 1nchaos
@time: 2023/6/5
@log: change log
"""
import copy
import datetime
import time

from adata.common import requests
from adata.common.headers import ths_headers


class BaseThs(object):
    """同花顺base类"""

    def __init__(self) -> None:
        super().__init__()

    def _get_text(self, api_url, code):
        """
        获取同花顺的请求 text
        :param api_url: url
        :param code: 代码
        :return:
        """
        headers = copy.deepcopy(ths_headers.text_headers)
        headers['Host'] = 'd.10jqka.com.cn'
        text = ''
        for i in range(2):
            res = requests.request('get', api_url, headers=headers, proxies={})
            text = res.text
            if code in text:
                break
            time.sleep(2)
        return text

    def _get_years_by_start_date(self, start_date):
        """
        根据开始时间获取年份
        :param start_date: 开始时间
        :return: 年份
        """
        years = []
        if not start_date:
            years.append('last')
        else:
            current_year = datetime.datetime.now().year
            start_year = datetime.datetime.strptime(start_date, "%Y-%m-%d").year
            while start_year <= current_year:
                years.append(start_year - 1)
                start_year += 1
            if current_year not in years:
                years.append(current_year)
        return years
