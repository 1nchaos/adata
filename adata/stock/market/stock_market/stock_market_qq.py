# -*- coding: utf-8 -*-
"""
@desc: 腾讯股票行情中心
https://stockapp.finance.qq.com/mstats/#

@author: 1nchaos
@time: 2023/6/19
@log: change log
"""
import pandas as pd

from adata.common import requests
from .stock_market_template import StockMarketTemplate


class StockMarketQQ(StockMarketTemplate):
    """
    腾讯股票行情
    """

    def __init__(self) -> None:
        super().__init__()

    def list_market_current(self, code_list=None):
        """
        获取多个股票最新行情信息
        https://qt.gtimg.cn/r=0.5979076524724433&q=s_sh600011,s_r_hk00902,s_sh600012,s_r_hk00995,s_sh600016,whHKDCNY
        :param code_list: 股票代码
        :return: 当前最新的行情价格信息
        """
        api_url = f"https://qt.gtimg.cn/r=0.5979076524724433&q="
        for code in code_list:
            if code.startswith('0') or code.startswith('3'):
                api_url += 's_sz' + code + ','
            elif code.startswith('6') or code.startswith('9'):
                api_url += 's_sh' + code + ','
            elif code.startswith('4') or code.startswith('8'):
                api_url += 's_bj' + code + ','

        # 1.请求接口
        res = requests.request('get', api_url, headers={})

        # 2. 判断结果是否正确
        if len(res.text) < 1 or res.status_code != 200:
            return pd.DataFrame(data=[], columns=self._MARKET_CURRENT_COLUMNS)
        # 3.解析数据

        # 正常解析数据 v_s_sz000936="51~华西股份~000936~12.60~1.15~10.04~69137~8711~~111.64~GP-A";
        data_list = res.text.split(';')
        data = []
        for data_str in data_list:
            if len(data_str) < 8:
                continue
            code = data_str.split('~')
            if len(code) == 11:
                data.append(code[1:8])

        # 4. 封装数据
        data_columns = ['short_name', 'stock_code', 'price', 'change', 'change_pct', 'volume', 'amount']
        result_df = pd.DataFrame(data=data, columns=data_columns)
        # 单位：手，万元
        mask = result_df['stock_code'].str.startswith(('0', '3', '6', '9'))
        result_df.loc[mask, 'volume'] = result_df['volume'].astype(int) * 100
        result_df.loc[mask, 'amount'] = result_df['amount'].astype(float) * 10000
        return result_df[self._MARKET_CURRENT_COLUMNS]


if __name__ == '__main__':
    print(StockMarketQQ().list_market_current(code_list=['000001', '600001', '000795', '872925']))
