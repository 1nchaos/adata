# -*- coding: utf-8 -*-
"""
@desc: adata
@author: 1nchaos
@time: 2023/4/4
"""
# -*- coding: utf-8 -*-

import logging

from .__version__ import __version__
from .bond import bond
from .fund import fund
from .sentiment import sentiment
from .stock import stock


def version():
    return __version__


# set up logging
logger = logging.getLogger("adata")


def set_logger():
    format_string = "%(asctime)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(format_string, datefmt="%Y-%m-%dT%H:%M:%S")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)


set_logger()
