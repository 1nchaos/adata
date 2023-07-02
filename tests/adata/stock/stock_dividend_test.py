# -*- coding: utf-8 -*-
"""
@desc: 
@author: 1nchaos
@time: 2023/7/2
@log: change log
"""
import adata

if __name__ == '__main__':
    res_df = adata.stock.market.get_dividend(stock_code='000001')
    print(res_df)
