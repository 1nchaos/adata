# -*- coding: utf-8 -*-
"""
@desc: adata
@author: 1nchaos
@time: 2023/4/4
"""
# -*- coding: utf-8 -*-

import logging  # noqa: F401  保留模块级 logging，兼容历史 adata.logging 用法

from adata.__version__ import __version__
from adata._logger import logger, set_logger
from adata.bond import bond
from adata.common.utils.sunrequests import SunProxy
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


# set up logging
# logger 与 set_logger 的实现见 adata/_logger.py，此处保持对外接口不变
set_logger()
