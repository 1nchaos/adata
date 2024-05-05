# -*- coding: utf-8 -*-
"""
@desc: 新浪
https://vip.stock.finance.sina.com.cn/mkt/#hskzz_z

@author: 1nchaos
@time:2023/4/5
@log: 
"""
import pandas as pd

from adata.bond.market.bond_market_template import BondMarketTemplate
from adata.common.utils import requests


class BondMarketSina(BondMarketTemplate):
    """bond 行情"""

    def __init__(self) -> None:
        super().__init__()

    def list_market_current(self, code_list=None):
        """
       获取新浪的最新可转债行情
       url : http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple
       :param code_list:  可转债代码列表
       :return: 最新行情数据
       """
        # 0.进行参数拼接处理
        api_url = f"http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple"

        # 2.循环请求
        data = []
        for i in range(100):
            # 1.请求接口
            params = {"page": {i}, "num": "80", "sort": "symbol",
                      "asc": "1", "node": "hskzz_z", "_s_r_a": "page"}
            res = requests.request('get', api_url, params=params)
            res = res.json()
            data.extend(res)
            if len(res) < 80:
                break
        # 3. 结果筛选
        if code_list is not None:
            new_data = []
            for d in data:
                if d['code'] in code_list:
                    new_data.append(d)
            data = new_data
        # 4. 封装数据
        rename = {'code': 'bond_code', 'name': 'bond_name', 'pricechange': 'change', 'changepercent': 'change_pct',
                  'settlement': 'pre_close', 'ticktime': 'time', 'trade': 'price'}
        result_df = pd.DataFrame(data=data).rename(columns=rename)
        columns_to_convert = ['price', 'open', 'high', 'low', 'pre_close', 'change', 'change_pct', 'volume', 'amount']
        result_df[columns_to_convert] = result_df[columns_to_convert].astype(float)
        return result_df[self._MARKET_CURRENT_COLUMNS]


if __name__ == '__main__':
    df = BondMarketSina().list_market_current()
    print(df)
