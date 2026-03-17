
# -*- coding: utf-8 -*-
"""
@desc: API请求限流中间件
@author: adata
@time: 2025/03/17
"""
import threading
import time
from collections import deque
from urllib.parse import urlparse


class RateLimiter:
    """
    基于域名的独立频率控制器
    滑动窗口算法实现，线程安全
    """
    
    def __init__(self):
        self._lock = threading.RLock()
        self._domain_limits = {}
        self._domain_windows = {}
        self._default_limit = 30
        self._default_window = 60
    
    def set_domain_limit(self, domain, limit, window=60):
        """
        设置特定域名的限流阈值
        :param domain: 域名（不带http/https）
        :param limit: 允许的请求次数
        :param window: 时间窗口（秒），默认60秒
        """
        with self._lock:
            self._domain_limits[domain] = (limit, window)
            if domain not in self._domain_windows:
                self._domain_windows[domain] = deque()
    
    def get_domain_limit(self, domain):
        """
        获取特定域名的限流阈值
        :param domain: 域名
        :return: (limit, window)
        """
        with self._lock:
            return self._domain_limits.get(domain, (self._default_limit, self._default_window))
    
    def set_default_limit(self, limit, window=60):
        """
        设置默认限流阈值
        :param limit: 默认允许的请求次数
        :param window: 时间窗口（秒）
        """
        with self._lock:
            self._default_limit = limit
            self._default_window = window
    
    def _clean_old_requests(self, domain, window, now):
        """
        清理过期的请求记录
        """
        window_start = now - window
        while len(self._domain_windows[domain]) > 0:
            if self._domain_windows[domain][0] <= window_start:
                self._domain_windows[domain].popleft()
            else:
                break
    
    def acquire(self, url):
        """
        请求限流，根据URL获取域名进行限制
        :param url: 请求的URL
        :return: 等待时间（秒），0表示不需要等待
        """
        domain = self._extract_domain(url)
        
        with self._lock:
            if domain not in self._domain_windows:
                self._domain_windows[domain] = deque()
            
            limit, window = self.get_domain_limit(domain)
            now = time.time()
            
            self._clean_old_requests(domain, window, now)
            
            if len(self._domain_windows[domain]) < limit:
                self._domain_windows[domain].append(now)
                return 0
            
            oldest_time = self._domain_windows[domain][0]
            wait_time = window - (now - oldest_time)
            if wait_time > 0:
                return wait_time
            else:
                self._domain_windows[domain].popleft()
                self._domain_windows[domain].append(now)
                return 0
    
    def _extract_domain(self, url):
        """
        从URL中提取域名
        """
        parsed = urlparse(url)
        return parsed.netloc


_rate_limiter_instance = None
_instance_lock = threading.Lock()


def get_rate_limiter():
    """
    获取单例限流器
    :return: RateLimiter 实例
    """
    global _rate_limiter_instance
    if _rate_limiter_instance is None:
        with _instance_lock:
            if _rate_limiter_instance is None:
                _rate_limiter_instance = RateLimiter()
    return _rate_limiter_instance


def set_domain_limit(domain, limit, window=60):
    """
    便捷函数：设置特定域名的限流阈值
    """
    get_rate_limiter().set_domain_limit(domain, limit, window)


def set_default_limit(limit, window=60):
    """
    便捷函数：设置默认限流阈值
    """
    get_rate_limiter().set_default_limit(limit, window)


def enable_rate_limit(enable=True):
    """
    启用或禁用全局限流功能
    :param enable: True启用，False禁用，默认True
    """
    from adata.common.utils.sunrequests import get_sun_requests
    sun_req = get_sun_requests(enable_rate_limit=enable)
    return sun_req

