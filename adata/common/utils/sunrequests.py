# -*- coding: utf-8 -*-
"""
@desc: adata 请求工具类
@author: 1nchaos
@time:2023/3/30
@log: 封装请求次数
"""

import time

import requests


class SunRequests(object):
    def __init__(self) -> None:
        super().__init__()

    def request(self, method='get', url=None, times=3, sleep_time=1588, **kwargs):
        """
        简单封装的请求，参考requests，增加循环次数和次数之间的等待时间
        :param method: 请求方法： get；post
        :param url: url
        :param times: 次数，int
        :param sleep_time: 循环的等待时间，毫秒
        :param kwargs: 其它 requests 参数，用法相同
        :return: res
        """
        res = None
        for i in range(times):
            res = requests.request(method=method, url=url, **kwargs)
            if res.status_code in (200, 404):
                return res
            time.sleep(sleep_time / 1000)
        return res
