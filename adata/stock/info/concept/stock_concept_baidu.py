# -*- coding: utf-8 -*-
"""
@summary: 股票概念
东方财富股票概念

https://data.eastmoney.com/bkzj/gn.html

单个股票的所有概念板块
https://datacenter.eastmoney.com/securities/api/data/v1/get?reportName=RPT_F10_CORETHEME_BOARDTYPE&columns=SECUCODE%2CSECURITY_CODE%2CSECURITY_NAME_ABBR%2CNEW_BOARD_CODE%2CBOARD_NAME%2CSELECTED_BOARD_REASON%2CIS_PRECISE%2CBOARD_RANK%2CBOARD_YIELD%2CDERIVE_BOARD_CODE&quoteColumns=f3~05~NEW_BOARD_CODE~BOARD_YIELD&filter=(SECUCODE%3D%22600138.SH%22)(IS_PRECISE%3D%221%22)&pageNumber=1&pageSize=&sortTypes=1&sortColumns=BOARD_RANK&source=HSF10&client=PC&v=0029565688091059528
@author: 1nchaos
@date: 2023/3/30 16:17
"""

import json
from urllib.parse import parse_qs

import pandas as pd

from adata.common import requests
from adata.common.headers import baidu_headers
from adata.stock.info.concept.stock_concept_template import StockConceptTemplate


class StockConceptBaidu(StockConceptTemplate):
    """
    股票概念
    """

    def __init__(self) -> None:
        super().__init__()

    def get_concept_baidu(self, stock_code='000001'):
        """
        根据股票代码获取，股票所属的所有的概念信息
        https://finance.pae.baidu.com/api/getrelatedblock?stock=[{"code":"300059","market":"ab","type":"stock"}]&finClientType=pc
        :param stock_code: 股票代码
        :return: 概念信息
        """
        # 1. 请求参数封装
        code_list = []
        if isinstance(stock_code, str):
            stock_code = [stock_code]
        for code in stock_code:
            code_list.append({"code": code, "market": "ab", "type": "stock"})
        url = f"""https://finance.pae.baidu.com/api/getrelatedblock?stock={json.dumps(code_list)}&finClientType=pc"""
        res_json = requests.request('get', url, headers=baidu_headers.json_headers, proxies={}).json()

        # 1. 返回结果判断
        if not res_json['Result']:
            return pd.DataFrame(data=[], columns=self._CONCEPT_INFO_COLUMNS)

        # 2. 正常返回数据结果封装
        res_json = res_json['Result']
        data = []
        for key, value in res_json.items():
            for concept_type in value:
                if concept_type['name'] == '概念':
                    for _ in concept_type['list']:
                        data.append({'stock_code': key, 'concept_code': parse_qs(_['xcx_query']).get('code', '')[0],
                                     'name': _['name'],
                                     'reason': '', 'source': '百度股市通'})
        result_df = pd.DataFrame(data=data, columns=self._CONCEPT_INFO_COLUMNS)
        return result_df


if __name__ == '__main__':
    print(StockConceptBaidu().get_concept_baidu(stock_code=["600020", '300059', '300033']).to_string())
