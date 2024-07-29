# -*- coding: utf-8 -*-
"""
@desc: 新浪
https://finance.sina.com.cn/stock/

@author: 1nchaos
@time: 2023/06/19
@log: change log
"""

import pandas as pd
from adata.common.exception.handler import handler_null

from adata.common.headers import sina_headers
from adata.common.utils import requests
from adata.stock.market.stock_market.stock_market_template import StockMarketTemplate


class StockMarketSina(StockMarketTemplate):
    """
    新浪股票行情
    """

    def __init__(self) -> None:
        super().__init__()

    @handler_null
    def list_market_current(self, code_list=None):
        """
        获取新浪的最新股票行情
        url : https://hq.sinajs.cn/list=s_sh600905,s_sz000725,s_sz000100,s_sh601919
        :param code_list:  代码列表
        :return: 最新行情数据：代码,简称,当前价格(元),涨跌额(元),涨跌幅(%),成交量(股),成交额(元)
        """
        # 0.进行参数拼接处理
        api_url = f"https://hq.sinajs.cn/list="
        for code in code_list:
            if code.startswith('0') or code.startswith('3'):
                api_url += 's_sz' + code + ','
            elif code.startswith('6') or code.startswith('9'):
                api_url += 's_sh' + code + ','
            elif code.startswith('4') or code.startswith('8'):
                api_url += 's_bj' + code + ','

        # 1.请求接口
        res = requests.request('get', api_url, headers=sina_headers.c_headers)

        # 2. 判断结果是否正确
        if len(res.text) < 1 or res.status_code != 200:
            return pd.DataFrame(data=[], columns=self._MARKET_CURRENT_COLUMNS)
        # 3.解析数据

        # 正常解析数据 var hq_str_s_bj872925="平安银行,14.840,0.480,3.343,374847,5483780.180";
        data_list = res.text.split(';')
        data = []
        for data_str in data_list:
            if len(data_str) < 8:
                continue
            idx = data_str.index('=')
            code = [data_str[idx - 6:idx]]
            code.extend(data_str[idx + 2:-1].split(','))
            if len(code) == 7:
                data.append(code)

        # 4. 封装数据
        result_df = pd.DataFrame(data=data, columns=self._MARKET_CURRENT_COLUMNS)
        # 北京的单位是股和万元
        mask = result_df['stock_code'].str.startswith(('0', '3', '6', '9'))
        result_df.loc[mask, 'volume'] = result_df['volume'].astype(int) * 100
        result_df.loc[mask, 'amount'] = result_df['amount'].astype(float) * 10000
        return result_df


if __name__ == '__main__':
    print(StockMarketSina().list_market_current(code_list=['000001', '600001', '000795', '872925']))
