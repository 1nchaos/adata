# -*- coding: utf-8 -*-
"""
@summary:
@author: 1nchaos
@date: 2023/7/2 07:51
"""
from adata import stock

if __name__ == '__main__':
    res_df = stock.market.get_market(stock_code='000100', k_type=1, start_date='2021-01-01')
    print(res_df)
