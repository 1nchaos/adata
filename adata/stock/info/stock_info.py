# -*- coding: utf-8 -*-
"""
@desc: 
@author: 1nchaos
@time:2024/4/23
@log: 
"""
import pandas as pd

from adata.common import requests
from adata.common.utils.code_utils import compile_exchange_by_stock_code


class StockInfo(object):
    __STOCK_SHARES_COLUMNS = ['stock_code', 'change_date', 'total_shares', 'limit_shares', 'list_a_shares',
                              'change_reason']

    def get_stock_shares(self, stock_code: str = '000033', is_history=True):
        """
        https://datacenter.eastmoney.com/securities/api/data/v1/get?reportName=RPT_F10_EH_EQUITY&columns=SECUCODE,SECURITY_CODE,END_DATE,TOTAL_SHARES,LIMITED_SHARES,LIMITED_OTHARS,LIMITED_DOMESTIC_NATURAL,LIMITED_STATE_LEGAL,LIMITED_OVERSEAS_NOSTATE,LIMITED_OVERSEAS_NATURAL,UNLIMITED_SHARES,LISTED_A_SHARES,B_FREE_SHARE,H_FREE_SHARE,FREE_SHARES,LIMITED_A_SHARES,NON_FREE_SHARES,LIMITED_B_SHARES,OTHER_FREE_SHARES,LIMITED_STATE_SHARES,LIMITED_DOMESTIC_NOSTATE,LOCK_SHARES,LIMITED_FOREIGN_SHARES,LIMITED_H_SHARES,SPONSOR_SHARES,STATE_SPONSOR_SHARES,SPONSOR_SOCIAL_SHARES,RAISE_SHARES,RAISE_STATE_SHARES,RAISE_DOMESTIC_SHARES,RAISE_OVERSEAS_SHARES,CHANGE_REASON&quoteColumns=&filter=(SECUCODE="688192.SH")&pageNumber=1&pageSize=20&sortTypes=-1&sortColumns=END_DATE&source=HSF10&client=PC&v=0656612716529632
        :param is_history: 是否获取历史 默认是
        :param stock_code: 股票代码
        :return:
        """
        stock_code = compile_exchange_by_stock_code(stock_code)
        url = f"""https://datacenter.eastmoney.com/securities/api/data/v1/get?reportName=RPT_F10_EH_EQUITY&columns=SECUCODE,SECURITY_CODE,END_DATE,TOTAL_SHARES,LIMITED_SHARES,LIMITED_OTHARS,LIMITED_DOMESTIC_NATURAL,LIMITED_STATE_LEGAL,LIMITED_OVERSEAS_NOSTATE,LIMITED_OVERSEAS_NATURAL,UNLIMITED_SHARES,LISTED_A_SHARES,B_FREE_SHARE,H_FREE_SHARE,FREE_SHARES,LIMITED_A_SHARES,NON_FREE_SHARES,LIMITED_B_SHARES,OTHER_FREE_SHARES,LIMITED_STATE_SHARES,LIMITED_DOMESTIC_NOSTATE,LOCK_SHARES,LIMITED_FOREIGN_SHARES,LIMITED_H_SHARES,SPONSOR_SHARES,STATE_SPONSOR_SHARES,SPONSOR_SOCIAL_SHARES,RAISE_SHARES,RAISE_STATE_SHARES,RAISE_DOMESTIC_SHARES,RAISE_OVERSEAS_SHARES,CHANGE_REASON&quoteColumns=&filter=(SECUCODE="{stock_code}")&pageNumber=1&pageSize=20&sortTypes=-1&sortColumns=END_DATE&source=HSF10&client=PC&v=0656612716529632"""
        res_json = requests.request('get', url, headers={}, proxies={}).json()
        # 1. 返回结果判断
        if not res_json['success']:
            return pd.DataFrame(data=[], columns=self.__STOCK_SHARES_COLUMNS)

        # 2. 正常返回数据结果封装
        res_data = res_json['result']['data']
        data = []
        for _ in res_data:
            data.append({'stock_code': _['SECURITY_CODE'], 'change_date': _['END_DATE'],
                         'total_shares': _['TOTAL_SHARES'],
                         'limit_shares': _['LIMITED_SHARES'],
                         'list_a_shares': int(_['LISTED_A_SHARES']) if _['LISTED_A_SHARES'] else _['LISTED_A_SHARES'],
                         'change_reason': _['CHANGE_REASON']})
        result_df = pd.DataFrame(data=data, columns=self.__STOCK_SHARES_COLUMNS)
        if not is_history:
            result_df = result_df.iloc[0:1]
        result_df['change_date'] = pd.to_datetime(result_df['change_date']).dt.strftime('%Y-%m-%d')
        return result_df


if __name__ == '__main__':
    print(StockInfo().get_stock_shares(stock_code='600001', is_history=True))
