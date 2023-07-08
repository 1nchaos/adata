# -*- coding: utf-8 -*-
import adata

if __name__ == '__main__':
    print(adata.version())
    # 代理
    adata.proxy(False)
    df = adata.stock.market.get_dividend(stock_code='000001')
    print(df)
