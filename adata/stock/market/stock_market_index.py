# -*- coding: utf-8 -*-
"""
@summary: 股票指数 行情
@author: 1nchaos
@date: 2023/06/01 16:17
"""
import copy
import time

from adata.common.headers import ths_headers
from adata.common.utils import requests, cookie


class StockMarketIndex(object):
    """
    股票指数 行情
    """
    COLUMNS = ['trade_date', 'open', 'high', 'low', 'close', 'volume', 'amount']

    def __init__(self) -> None:
        super().__init__()

    def get_market_index(self, index_code: str = '886013', start_date='2020-01-01', k_type: int = 1):
        """
        获取指数行情
        """
        res_df = self.__get_market_index_ths(index_code=index_code, k_type=k_type)
        return res_df

    def __get_market_index_ths(self, index_code: str = '000001', k_type: int = 1, adjust_type: int = 1):
        pass

    def __get_market_index_min_ths(self, index_code):
        pass

    def __get_market_index_today_ths(self, index_code: str = '886013', k_type: int = 1, adjust_type: int = 1):
        pass

    def __get_text(self, api_url, code):
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


if __name__ == '__main__':
    print(StockMarketIndex().get_market_index(index_code='000001'))
    # print(StockMarketIndex().get_market_concept_min_ths(index_code='886041'))
    # print(StockMarketIndex().get_market_concept_today_ths(index_code='886041'))
