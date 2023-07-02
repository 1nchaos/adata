# -*- coding: utf-8 -*-
"""
@summary:
@author: 1nchaos
@date: 2023/7/2 07:51
"""
import adata

if __name__ == '__main__':
    res_df = adata.stock.market.get_market(stock_code='000100', k_type=1, start_date='2021-01-01')
    print(res_df)
    res_df = adata.stock.market.get_market(stock_code='000001', start_date='2021-01-01', k_type=1)
    print(res_df)
    res_df = adata.stock.market.get_market_min(stock_code='000001')
    print(res_df)
    res_df = adata.stock.market.list_market_current(code_list=['000001', '600001', '000795', '872925'])
    print(res_df)
