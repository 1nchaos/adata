# -*- coding: utf-8 -*-
"""
@desc: adata
@author: 1nchaos
@time: 2023/4/4
"""
# -*- coding: utf-8 -*-

import logging
from typing import Optional

from adata.__version__ import __version__
from adata.bond import bond
from adata.common.utils.rate_limiter import (
    get_rate_limiter,
    set_rate_limit,
    set_default_rate_limit,
    get_stats as get_rate_limit_stats,
    reset_rate_limiter,
)
from adata.common.utils.sunrequests import SunProxy, sun_requests
from adata.fund import fund
from adata.sentiment import sentiment
from adata.stock import stock


def version():
    return __version__


def proxy(is_proxy=False, ip: str = None, proxy_url: str = None):
    """
    设置请求代理
    :param is_proxy: 是否启用代理，默认：否
    :param ip: 代理ip地址；格式样例：192.123.123.4:4568
    :param proxy_url: 能获取到代理的url，返回格式必须和ip一样
    """
    SunProxy.set('is_proxy', is_proxy)
    SunProxy.set('ip', ip)
    SunProxy.set('proxy_url', proxy_url)
    return


def rate_limit(domain: str, max_requests: int = 30, time_window: int = 60) -> None:
    """
    设置特定域名的请求限流参数

    用于控制对特定数据源的请求频率，防止因高频请求导致的IP封禁或API配额耗尽。
    采用滑动窗口算法，确保在任意 time_window 秒内不超过 max_requests 次请求。

    :param domain: 域名，如 "eastmoney.com", "push2his.eastmoney.com"
    :param max_requests: 时间窗口内最大请求数，默认30次
    :param time_window: 时间窗口（秒），默认60秒

    示例:
        >>> import adata
        >>> # 设置东方财富接口每分钟最多请求30次
        >>> adata.rate_limit("eastmoney.com", max_requests=30, time_window=60)
        >>> # 设置更严格的限制：每分钟20次
        >>> adata.rate_limit("push2his.eastmoney.com", max_requests=20, time_window=60)
        >>> # 查询股票行情（会自动应用限流）
        >>> df = adata.stock.market.get_market(stock_code='000001', k_type=1)
    """
    set_rate_limit(domain, max_requests=max_requests, time_window=time_window)


def rate_limit_default(max_requests: int = 30, time_window: int = 60) -> None:
    """
    设置默认的请求限流参数

    对所有未单独配置限流参数的域名生效。

    :param max_requests: 默认时间窗口内最大请求数，默认30次
    :param time_window: 默认时间窗口（秒），默认60秒

    示例:
        >>> import adata
        >>> # 设置默认每分钟最多请求20次
        >>> adata.rate_limit_default(max_requests=20, time_window=60)
    """
    set_default_rate_limit(max_requests=max_requests, time_window=time_window)


def rate_limit_enable() -> None:
    """启用请求限流器（默认已启用）"""
    sun_requests.enable_rate_limit()
    logger.info("[RateLimiter] 请求限流已启用")


def rate_limit_disable() -> None:
    """禁用请求限流器"""
    sun_requests.disable_rate_limit()
    logger.info("[RateLimiter] 请求限流已禁用")


def rate_limit_stats(domain: Optional[str] = None) -> dict:
    """
    获取限流统计信息

    :param domain: 指定域名，None表示返回所有域名统计
    :return: 统计信息字典

    示例:
        >>> import adata
        >>> # 查看所有域名统计
        >>> stats = adata.rate_limit_stats()
        >>> print(stats)
        >>> # 查看特定域名统计
        >>> stats = adata.rate_limit_stats("eastmoney.com")
        >>> print(stats)
    """
    return get_rate_limit_stats(domain)


def rate_limit_reset(domain: Optional[str] = None) -> None:
    """
    重置限流器状态

    :param domain: 指定域名，None表示重置所有域名

    示例:
        >>> import adata
        >>> # 重置特定域名
        >>> adata.rate_limit_reset("eastmoney.com")
        >>> # 重置所有域名
        >>> adata.rate_limit_reset()
    """
    reset_rate_limiter(domain)


# set up logging
logger = logging.getLogger("adata")


def set_logger():
    format_string = "%(asctime)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(format_string, datefmt="%Y-%m-%dT%H:%M:%S")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)


set_logger()
