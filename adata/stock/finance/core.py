# -*- coding: utf-8 -*-
"""
@desc: 主要指标
https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=SZ300059&color=b#/cwfx/zyzb

@author: 1nchaos
@time: 2024/9/3
@log: change log
"""
import pandas as pd

from adata.common import requests
from adata.common.utils.code_utils import compile_exchange_by_stock_code


class Core(object):
    def __init__(self) -> None:
        pass

    def get_core_index(self, stock_code='300059'):
        """核心指标"""
        return self.__core_index_east(stock_code)

    def __core_index_east(self, stock_code='300059'):
        """东方财富"""
        # 1. 参数设置
        report_type = ['年报', '中报', '三季报', '一季报']
        stock_code = compile_exchange_by_stock_code(stock_code)

        # 2. 请求url
        data = []
        for i in report_type:
            url = f'https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_F10_FINANCE_MAINFINADATA&' \
                  f'sty=APP_F10_MAINFINADATA&quoteColumns=&filter=(SECUCODE="{stock_code}")(REPORT_TYPE="{i}")&' \
                  f'p=1&ps=100&sr=-1&st=REPORT_DATE&source=HSF10&client=PC&v=03890754131799983'
            r = requests.request(method='get', url=url, timeout=30)

            # 3. 解析数据
            data_json = r.json()
            code = data_json['code']
            if code == 0:
                res = data_json["result"]["data"]
                data.extend(res)
        # 4. 数据etl
        rename = {
            'SECURITY_CODE': 'stock_code',
            'SECURITY_NAME_ABBR': 'short_name',
            'REPORT_DATE': 'report_date',
            'REPORT_TYPE': 'report_type',
            'NOTICE_DATE': 'notice_date',

            'EPSJB': 'epsjb',
            'EPSKCJB': 'epskcjb',
            'EPSXS': 'epsxs',
            'BPS': 'bps',
            'MGZBGJ': 'mgzbgj',
            'MGWFPLR': 'total_share',
            'MGJYXJJE': 'total_share',

            "TOTALOPERATEREVE": 'totaloperatereve',
            "MLR": "mlr",
            "PARENTNETPROFIT": "parentnetprofit",
            "KCFJCXSYJLR": "kcfjcxsyjlr",
            "TOTALOPERATEREVETZ": "totaloperaterevetz",
            "PARENTNETPROFITTZ": "parentnetprofittz",
            "KCFJCXSYJLRTZ": "kcfjcxsyjlrtz",
            "YYZSRGDHBZC": "yyzsrgdhbzc",
            "NETPROFITRPHBZC": "netprofitrphbzc",
            "KFJLRGDHBZC": "kfjlrgdhbzc",

            "ROEJQ": "roejq",
            "ROEKCJQ": "roekcjq",
            "ZZCJLL": "zzcjll",
            "XSMLL": "xsmll",
            "XSJLL": "xsjll",

            "YSZKYYSR": 'yszkyysr',
            "XSJXLYYSR": 'xsjxlyysr',
            "JYXJLYYSR": 'jyxjlyysr',
            "TAXRATE": 'taxrate',

            "LD": 'ld',
            "SD": 'sd',
            "XJLLB": 'xjllb',
            "ZCFZL": 'zcfzl',
            "QYCS": 'qycs',
            "CQBL": 'cqbl',

            "ZZCZZTS": 'zzczzts',
            "CHZZTS": 'chzzts',
            "YSZKZZTS": 'yszkzzts',
            "TOAZZL": 'toazzl',
            "CHZZL": 'chzzl',
            "YSZKZZL": 'yszkzzl',
        }
        df = pd.DataFrame(data).rename(columns=rename)[rename.values()]
        df['report_date'] = pd.to_datetime(df['report_date']).dt.strftime('%Y-%m-%d')
        df = df.sort_values(by='report_date', ascending=False)
        return df


if __name__ == '__main__':
    print(Core().get_core_index('300059'))
