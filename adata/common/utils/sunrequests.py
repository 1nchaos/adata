# -*- coding: utf-8 -*-
"""
代理:https://jahttp.zhimaruanjian.com/getapi/

@desc: adata 请求工具类
@author: 1nchaos
@time:2023/3/30
@log: 封装请求次数
"""

import threading
import time

import requests

from adata._logger import get_logger

logger = get_logger(__name__)

DEFAULT_TIMEOUT = 15
"""默认单次请求超时时间（秒）：避免数据源无响应时调用方被无限阻塞"""
_PROXY_FETCH_TIMEOUT = 5
"""获取代理 ip 的超时时间（秒）"""


class SunProxy(object):
    """代理配置单例：存放 is_proxy、ip、proxy_url 等全局配置"""

    _data = {}
    _instance = None
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = object.__new__(cls)
        return cls._instance

    @classmethod
    def set(cls, key, value):
        cls._data[key] = value

    @classmethod
    def get(cls, key):
        return cls._data.get(key)

    @classmethod
    def delete(cls, key):
        if key in cls._data:
            del cls._data[key]


class SunRequests(object):
    def __init__(self, sun_proxy: SunProxy = None) -> None:
        super().__init__()
        self.sun_proxy = sun_proxy

    def request(self, method='get', url=None, times=3, retry_wait_time=1588, proxies=None, wait_time=None,
                timeout=DEFAULT_TIMEOUT, **kwargs):
        """
        简单封装的请求，参考requests，增加循环次数和次数之间的等待时间
        :param proxies: 代理配置
        :param method: 请求方法： get；post
        :param url: url
        :param times: 次数，int
        :param retry_wait_time: 重试等待时间，毫秒
        :param wait_time: 等待时间：毫秒；表示每个请求的间隔时间，在请求之前等待sleep，主要用于防止请求太频繁的限制。
        :param timeout: 单次请求超时时间，秒；默认 15 秒
        :param kwargs: 其它 requests 参数，用法相同
        :return: res
        """
        # 1. 获取设置代理
        proxies = self.__get_proxies(proxies)
        # 2. 请求数据结果
        res = None
        for i in range(times):
            if wait_time:
                time.sleep(wait_time / 1000)
            res = requests.request(method=method, url=url, proxies=proxies, timeout=timeout, **kwargs)
            if res.status_code in (200, 404):
                return res
            # 4xx（429 限流除外）属确定性错误，重试不会改变结果，直接返回避免无意义等待
            if 400 <= res.status_code < 500 and res.status_code != 429:
                logger.warning("请求被拒绝，不再重试，status_code=%s，url=%s", res.status_code, url)
                return res
            logger.warning("请求异常，第 %s/%s 次，status_code=%s，url=%s", i + 1, times, res.status_code, url)
            if i < times - 1:
                time.sleep(retry_wait_time / 1000)
        return res

    def __get_proxies(self, proxies):
        """
        获取代理配置
        """
        if proxies is None:
            proxies = {}
        is_proxy = SunProxy.get('is_proxy')
        ip = SunProxy.get('ip')
        proxy_url = SunProxy.get('proxy_url')
        if not ip and is_proxy and proxy_url:
            ip = requests.get(url=proxy_url, timeout=_PROXY_FETCH_TIMEOUT).text.replace('\r\n', '') \
                .replace('\r', '').replace('\n', '').replace('\t', '')
        if is_proxy and ip:
            if ip.startswith('http'):
                proxies = {'https': f"{ip}", 'http': f"{ip}"}
            else:
                proxies = {'https': f"http://{ip}", 'http': f"http://{ip}"}
        return proxies


sun_requests = SunRequests()
