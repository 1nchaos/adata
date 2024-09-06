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

            'EPSJB': 'basic_eps',
            'EPSKCJB': 'diluted_eps',
            'EPSXS': 'non_gaap_eps',
            'BPS': 'net_asset_ps',
            'MGZBGJ': 'cap_reserve_ps',
            'MGWFPLR': 'undist_profit_ps',
            'MGJYXJJE': 'oper_cf_ps',

            "TOTALOPERATEREVE": 'total_rev',
            "MLR": "gross_profit",
            "PARENTNETPROFIT": "net_profit_attr_sh",
            "KCFJCXSYJLR": "non_gaap_net_profit",
            "TOTALOPERATEREVETZ": "total_rev_yoy_gr",
            "PARENTNETPROFITTZ": "net_profit_yoy_gr",
            "KCFJCXSYJLRTZ": "non_gaap_net_profit_yoy_gr",
            "YYZSRGDHBZC": "total_rev_qoq_gr",
            "NETPROFITRPHBZC": "net_profit_qoq_gr",
            "KFJLRGDHBZC": "non_gaap_net_profit_qoq_gr",

            "ROEJQ": "roe_wtd",
            "ROEKCJQ": "roe_non_gaap_wtd",
            "ZZCJLL": "roa_wtd",
            "XSMLL": "gross_margin",
            "XSJLL": "net_margin",

            "YSZKYYSR": 'adv_receipts_to_rev',
            "XSJXLYYSR": 'net_cf_sales_to_rev',
            "JYXJLYYSR": 'oper_cf_to_rev',
            "TAXRATE": 'eff_tax_rate',

            "LD": 'curr_ratio',
            "SD": 'quick_ratio',
            "XJLLB": 'cash_flow_ratio',
            "ZCFZL": 'asset_liab_ratio',
            "QYCS": 'equity_multiplier',
            "CQBL": 'equity_ratio',

            "ZZCZZTS": 'total_asset_turn_days',
            "CHZZTS": 'inv_turn_days',
            "YSZKZZTS": 'acct_recv_turn_days',
            "TOAZZL": 'total_asset_turn_rate',
            "CHZZL": 'inv_turn_rate',
            "YSZKZZL": 'acct_recv_turn_rate',
        }
        df = pd.DataFrame(data).rename(columns=rename)[rename.values()]
        df['report_date'] = pd.to_datetime(df['report_date']).dt.strftime('%Y-%m-%d')
        df['notice_date'] = pd.to_datetime(df['notice_date']).dt.strftime('%Y-%m-%d')
        df = df.sort_values(by='report_date', ascending=False)
        return df


if __name__ == '__main__':
    print(Core().get_core_index('300033'))
