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

try:
    from adata.common.utils.rate_limiter import get_rate_limiter
    _RATE_LIMIT_AVAILABLE = True
except ImportError:
    _RATE_LIMIT_AVAILABLE = False


class SunProxy(object):
    _data = {}
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(SunProxy, "_instance"):
            with SunProxy._instance_lock:
                if not hasattr(SunProxy, "_instance"):
                    SunProxy._instance = object.__new__(cls)

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
    def __init__(self, sun_proxy: SunProxy = None, enable_rate_limit=False) -&gt; None:
        super().__init__()
        self.sun_proxy = sun_proxy
        self.enable_rate_limit = enable_rate_limit

    def request(self, method='get', url=None, times=3, retry_wait_time=1588, proxies=None, wait_time=None, **kwargs):
        """
        简单封装的请求，参考requests，增加循环次数和次数之间的等待时间
        :param proxies: 代理配置
        :param method: 请求方法： get；post
        :param url: url
        :param times: 次数，int
        :param retry_wait_time: 重试等待时间，毫秒
        :param wait_time: 等待时间：毫秒；表示每个请求的间隔时间，在请求之前等待sleep，主要用于防止请求太频繁的限制。
        :param kwargs: 其它 requests 参数，用法相同
        :return: res
        """
        # 限流检查
        if self.enable_rate_limit and _RATE_LIMIT_AVAILABLE and url:
            limiter = get_rate_limiter()
            wait_limit = limiter.acquire(url)
            if wait_limit &gt; 0:
                domain = limiter._extract_domain(url)
                limit, window = limiter.get_domain_limit(domain)
                print("[RateLimit] 域名 %s 已达到 %d 次/%d 秒限制，等待 %.2f 秒..." % (domain, limit, window, wait_limit))
                time.sleep(wait_limit)
        
        # 1. 获取设置代理
        proxies = self.__get_proxies(proxies)
        # 2. 请求数据结果
        res = None
        for i in range(times):
            if wait_time:
                time.sleep(wait_time / 1000)
            res = requests.request(method=method, url=url, proxies=proxies, **kwargs)
            if res.status_code in (200, 404):
                return res
            time.sleep(retry_wait_time / 1000)
            if i == times - 1:
                return res
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
            ip = requests.get(url=proxy_url).text.replace('\r\n', '') \
                .replace('\r', '').replace('\n', '').replace('\t', '')
        if is_proxy and ip:
            if ip.startswith('http'):
                proxies = {'https': "%s" % ip, 'http': "%s" % ip}
            else:
                proxies = {'https': "http://%s" % ip, 'http': "http://%s" % ip}
        return proxies


_sun_requests = None
_sun_requests_lock = threading.Lock()


def get_sun_requests(enable_rate_limit=False):
    """
    获取 SunRequests 全局实例
    :param enable_rate_limit: 是否启用限流，默认False
    :return: SunRequests 实例
    """
    global _sun_requests
    if _sun_requests is None:
        with _sun_requests_lock:
            if _sun_requests is None:
                _sun_requests = SunRequests(enable_rate_limit=enable_rate_limit)
    elif _sun_requests.enable_rate_limit != enable_rate_limit:
        _sun_requests.enable_rate_limit = enable_rate_limit
    return _sun_requests


sun_requests = get_sun_requests()

