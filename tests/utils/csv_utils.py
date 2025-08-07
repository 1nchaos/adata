# -*- coding: utf-8 -*-
"""
@desc: trade_calendar_csv 生成
@author: 1nchaos
@time:2023/7/6
@log: 
"""
import pandas as pd

import adata


def calendar_csv():
    for i in range(1):
        year = 2025 - i
        df = adata.stock.info.trade_calendar(year=year)
        df.to_csv(f'{year}.csv', index=False)


def code_csv():
    sh = pd.read_excel('sh.xlsx')[['A股代码', '证券简称', '上市日期']]
    sh['上市日期'] = pd.to_datetime(sh['上市日期'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
    sz = pd.read_excel('sz.xlsx')[['A股代码', 'A股简称', 'A股上市日期']].rename(columns={'A股简称': '证券简称', 'A股上市日期': '上市日期'})
    code = pd.concat([sh, sz]).rename(columns={'A股代码': 'stock_code', '上市日期': 'list_date2', '证券简称': 'short_name'})
    code['stock_code'] = code['stock_code'].astype(str).str.zfill(6)
    code.to_csv(f'code.csv', index=False)
    print(code)


def f2csv():
    df = adata.stock.info.all_code()
    df.to_csv(f'all_code.csv', index=False)


if __name__ == '__main__':
    # code_csv()
    f2csv()
