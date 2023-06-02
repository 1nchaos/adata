# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/6/2
@log: change log
"""
import json

from adata.stock.info.stock_index import StockIndex

if __name__ == '__main__':
    index_code = StockIndex().all_index_code()
    rel = {}
    for row in index_code.itertuples():
        # 在这里使用 row.column_name 访问每一列的值
        if row.index_code != row.concept_code:
            rel[row.index_code] = row.concept_code
            rel[row.concept_code] = row.index_code
    with open('index_code_rel_ths.json', 'w') as f:
        json.dump(rel, f)
    print(rel)
