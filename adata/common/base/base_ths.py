# -*- coding: utf-8 -*-
"""
@desc: 同花顺基础类
@author: 1nchaos
@time: 2023/6/5
@log: change log
"""
import copy
import datetime
import re
import time

from bs4 import BeautifulSoup
from py_mini_racer import py_mini_racer

from adata.common import requests
from adata.common.headers import ths_headers
from adata.common.utils import cookie
from adata.common.utils.cookie import get_file_content_ths


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
        headers['Cookie'] = cookie.ths_cookie()
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
        根据开始时间获取大于开始时间的所有年份的列表
        例：start_date=2020-10-01 -> years=[2020,2021,2022,2023]
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

    def get_wencai_server_time(self):
        """
        获取问财服务时间
        :return: time
        """
        url = 'http://www.iwencai.com/unifiedwap/home/index'
        resp = requests.request(method='get', url=url)
        resp_text = resp.text
        soup = BeautifulSoup(resp_text, 'html.parser')
        js_url = "http:" + soup.find('script')['src']
        js_resp = requests.request(method='get', url=js_url)
        js_text = js_resp.text
        obj = re.compile(r'var TOKEN_SERVER_TIME=(?P<time>.*?);!function')
        server_time = obj.search(js_text).group('time')
        return server_time

    def wencai_hexin_v(self, js_path="hexin.js"):
        """
        wencai_hexin
        """
        js_code = py_mini_racer.MiniRacer()
        js_content = get_file_content_ths(file_path=js_path)
        js_content = 'var TOKEN_SERVER_TIME=' + str(self.get_wencai_server_time()) + ";\n" + js_content
        js_code.eval(js_content)
        v = js_code.call("rt.updata")
        return v


if __name__ == '__main__':
    print(BaseThs().wencai_hexin_v())
