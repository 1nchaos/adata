# -*- coding: utf-8 -*-
"""
@desc: trade_calendar_csv 生成
@author: 1nchaos
@time:2023/7/6
@log: 
"""
import adata

if __name__ == '__main__':
    for i in range(20):
        year = 2013 - i
        df = adata.stock.info.trade_calendar(year=year)
        df.to_csv(f'{year}.csv', index=False)
