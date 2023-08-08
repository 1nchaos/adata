# -*- coding: utf-8 -*-
"""
@summary: 股票概念
东方财富股票概念

https://data.eastmoney.com/bkzj/gn.html
@author: 1nchaos
@date: 2023/3/30 16:17
"""

import pandas as pd

from adata.common import requests
from adata.stock.info.concept.stock_concept_template import StockConceptTemplate


class StockConceptEast(StockConceptTemplate):
    """
    东方财富股票概念
    """

    def __init__(self) -> None:
        super().__init__()

    def all_concept_code_east(self):
        """
        https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=1000&po=1&np=1&fields=f12%2Cf13%2Cf14%2Cf62&fid=f62&fs=m%3A90%2Bt%3A3
        :return: 概念[[name,index_code，concept_code]]
        """
        url = f"https://push2.eastmoney.com/api/qt/clist/get" \
              f"?pn=1&pz=1000&po=1&np=1&fields=f12%2Cf13%2Cf14%2Cf62&fid=f62&fs=m%3A90%2Bt%3A3"
        res_json = requests.request('get', url, headers={}, proxies={}).json()
        res_data = res_json['data']['diff']
        data = []
        for _ in res_data:
            data.append({'index_code': _['f12'], 'concept_code': _['f12'], 'name': _['f14'], 'source': '东方财富'})
        result_df = pd.DataFrame(data=data, columns=self._CONCEPT_CODE_COLUMNS)
        return result_df

    def concept_constituent_east(self, concept_code=None, wait_time=None):
        """
        https://data.eastmoney.com/bkzj/BK1085.html
        https://push2.eastmoney.com/api/qt/clist/get?fid=f62&po=1&pz=1000&pn=1&np=1&fltt=2&invt=2&fs=b:BK0966&fields=f12,f14
        :param wait_time: 等待时间：毫秒；表示每个请求的间隔时间，主要用于防止请求太频繁的限制。
        :param concept_code: 概念代码，BK开头
        :return: 概念的成分股
        """
        curr_page = 1
        data = []
        while curr_page < 6:
            url = f"https://push2.eastmoney.com/api/qt/clist/get" \
                  f"?fid=f62&po=1&pz=1000&pn={curr_page}&np=1&fltt=2&invt=2&fs=b:{concept_code}&fields=f12,f14"
            res_json = requests.request('get', url, headers={}, proxies={}, wait_time=wait_time).json()
            res_data = res_json['data']
            if not res_data:
                break
            res_data = res_data['diff']
            for _ in res_data:
                data.append({'stock_code': _['f12'], 'short_name': _['f14']})
            curr_page += 1
        result_df = pd.DataFrame(data=data, columns=self._CONCEPT_CONSTITUENT_COLUMNS)
        return result_df


if __name__ == '__main__':
    print(StockConceptEast().all_concept_code_east())
    print(StockConceptEast().concept_constituent_east(concept_code="BK0637"))
