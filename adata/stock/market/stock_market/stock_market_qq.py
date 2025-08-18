# -*- coding: utf-8 -*-
"""
@desc: 腾讯股票行情中心
https://stockapp.finance.qq.com/mstats/#

@author: 1nchaos
@time: 2023/6/19
@log: change log
"""
import pandas as pd
from adata.common.exception.handler import handler_null

from adata.common import requests
from adata.common.utils.code_utils import get_exchange_by_stock_code
from adata.stock.market.stock_market.stock_market_template import StockMarketTemplate


class StockMarketQQ(StockMarketTemplate):
    """
    腾讯股票行情
    """

    def __init__(self) -> None:
        super().__init__()

    @handler_null
    def list_market_current(self, code_list=None):
        """
        获取多个股票最新行情信息
        https://qt.gtimg.cn/r=0.5979076524724433&q=s_sh600011,s_r_hk00902,s_sh600012,s_r_hk00995,s_sh600016,whHKDCNY
        :param code_list: 股票代码
        :return: 当前最新的行情价格信息
        """
        api_url = f"https://qt.gtimg.cn/r=0.5979076524724433&q="
        for code in code_list:
            api_url += f's_{get_exchange_by_stock_code(code).lower()}{code},'

        # 1.请求接口
        res = requests.request('get', api_url, headers={})

        # 2. 判断结果是否正确
        if len(res.text) < 1 or res.status_code != 200:
            return pd.DataFrame(data=[], columns=self._MARKET_CURRENT_COLUMNS)
        # 3.解析数据

        # 正常解析数据 v_s_sz000936="51~华西股份~000936~12.60~1.15~10.04~69137~8711~~111.64~GP-A";
        data_list = res.text.split(';')
        data = []
        for data_str in data_list:
            if len(data_str) < 8:
                continue
            code = data_str.split('~')
            if len(code) == 11:
                data.append(code[1:8])

        # 4. 封装数据
        data_columns = ['short_name', 'stock_code', 'price', 'change', 'change_pct', 'volume', 'amount']
        result_df = pd.DataFrame(data=data, columns=data_columns)
        # 单位：手，万元
        mask = result_df['stock_code'].str.startswith(('0', '3', '6', '9'))
        result_df.loc[mask, 'volume'] = result_df['volume'].astype(int) * 100
        result_df.loc[mask, 'amount'] = result_df['amount'].astype(float) * 10000
        return result_df[self._MARKET_CURRENT_COLUMNS]

    @handler_null
    def get_market_five(self, stock_code: str = '000001'):
        """
         https://web.sqt.gtimg.cn/q=sh601666,sh600691
        :param stock_code: 股票代码
        :return:
        """
        return self.list_market_five([stock_code])

    @handler_null
    def list_market_five(self, code_list=None):
        """
         https://web.sqt.gtimg.cn/q=sh601666,sh600691
        :param code_list: 股票代码列表
        :return:
        """
        if code_list is None or len(code_list) == 0:
            return pd.DataFrame(data=[], columns=self._MARKET_FIVE_COLUMNS)
        api_url = f"https://web.sqt.gtimg.cn/q="
        for code in code_list:
            api_url += f'{get_exchange_by_stock_code(code).lower()}{code},'

        # 1.请求接口
        res = requests.request('get', api_url, headers={})

        # 2. 判断结果是否正确
        if len(res.text) < 1 or res.status_code != 200:
            return pd.DataFrame(data=[], columns=self._MARKET_FIVE_COLUMNS)
        # 3.解析数据

        # 正常解析数据 _sh601666="1~平煤股份~601666~10.13~9.82~9.82~545608~302942~242666~10.12~1000~10.11~471~10.10~2083~10.09
        # ~989~10.08~632~10.13~2544~10.14~2794~10.15~3149~10.16~2103~10.17~1430~~20230913155915~0.31~3.16~10.23~9.82
        # ~10.13/545608/551678149~545608~55168~2.37~5.10~~10.23~9.82~4.18~233.15~234.39~1.08~10.80~8.84~1.05~-6845~10
        # .11~5.25~4.09~~~1.16~55167.8149~0.0000~0~
        # ~GP-A~1.91~1.81~8.59~19.02~6.34~13.52~7.21~19.60~31.56~34.53~2301581075~2313866675~-39.81~-4.70~2301581075
        # ~~~-22.43~0.10~~CNY~0~___D__F__N";
        data_list = res.text.split(';')
        data = []
        for data_str in data_list:
            if len(data_str) < 8:
                continue
            code = data_str.split('~')

            if len(code) >= 85:
                row = code[2:3]
                row.append(code[1])
                row.extend(code[27:29])
                row.extend(code[25:27])
                row.extend(code[23:25])
                row.extend(code[21:23])
                row.extend(code[19:21])
                row.extend(code[9:19])
                data.append(row)

        # 4. 封装数据
        result_df = pd.DataFrame(data=data, columns=self._MARKET_FIVE_COLUMNS)
        columns_to_multiply = ['sv5', 'sv4', 'sv3', 'sv2', 'sv1', 'bv1', 'bv2', 'bv3', 'bv4', 'bv5']
        result_df[columns_to_multiply] = result_df[columns_to_multiply].astype(int) * 100
        return result_df

    @handler_null
    def get_market_bar(self, stock_code: str = '000001'):
        """
        https://gu.qq.com/sh601857/gp/detail
        :param stock_code: 股票代码
        :return:
        """
        # 1. 参数处理
        code = get_exchange_by_stock_code(stock_code).lower()+stock_code
        res_df = pd.DataFrame()

        # 2. 请求接口
        for page in range(0, 10000):
            url = "http://stock.gtimg.cn/data/index.php"
            params = {
                "appn": "detail",
                "action": "data",
                "c": code,
                "p": page,
            }
            try:
                text = requests.request(method='get', url=url, params=params).text
                df = pd.DataFrame(eval(text[text.find("["):])[1].split("|")).iloc[:, 0].str.split("/", expand=True)
                if df.empty:
                    break
            except:
                break
            res_df = pd.concat([res_df, df], ignore_index=True)
        if res_df.empty:
            return pd.DataFrame(data=[], columns=self._MARKET_BAR_COLUMNS)

        # 3. 数据etl
        # big_df = res_df.iloc[:, 1:].copy()
        res_df.reset_index(drop=True, inplace=True)
        res_df.columns = ['no', "trade_time", "price", "1", "volume", "2", "bs_type"]

        res_df["stock_code"] = stock_code
        res_df = res_df.astype({"trade_time": str, "price": float, "volume": int, "bs_type": str, })
        return res_df[self._MARKET_BAR_COLUMNS]


if __name__ == '__main__':
    print(StockMarketQQ().list_market_current(code_list=['000001', '600001', '000795', '872925', '920445']))
    print(StockMarketQQ().get_market_five(stock_code='000001'))
    print(StockMarketQQ().get_market_bar(stock_code='000001'))
    print(StockMarketQQ().list_market_five(code_list=['000001', '872925', '920445']))
