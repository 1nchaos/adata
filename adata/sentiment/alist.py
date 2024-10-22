# -*- coding: utf-8 -*-
"""
@desc:  龙虎榜单

https://data.eastmoney.com/stock/tradedetail.html

@author: 1nchaos
@time: 2024/5/29
@log: change log
"""
import datetime
import json

import pandas as pd

from adata.common.base.base_ths import BaseThs
from adata.common.utils import requests


class AList(BaseThs):
    """龙虎榜单"""

    __A_LIST_DAILY_COLUMNS = [
        "trade_date",
        "short_name",
        "stock_code",
        "close",
        "change_cpt",
        "turnover_ratio",
        "a_net_amount",
        "a_buy_amount",
        "a_sell_amount",
        "a_amount",
        "amount",
        "net_amount_rate",
        "a_amount_rate",
        "reason",
    ]

    __A_LIST_INFO_COLUMNS = [
        "trade_date",
        "stock_code",
        "operate_code",
        "operate_name",
        "a_buy_amount",
        "a_sell_amount",
        "a_net_amount",
        "a_buy_amount_rate",
        "a_sell_amount_rate",
        "reason",
    ]

    # 东方财富人气榜
    def list_a_list_daily(self, report_date=None):
        """
        每日龙虎榜，默认为当天
        http://guba.eastmoney.com/rank/
        :param report_date: 报告日期 格式：YYYY-MM-DD
        """
        if report_date is None:
            report_date = datetime.datetime.now().strftime("%Y-%m-%d")
        # 1.url
        url = f"https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123047223270591945665_1716975719487&sortColumns=SECURITY_CODE,TRADE_DATE&sortTypes=1,-1&pageSize=500&pageNumber=1&reportName=RPT_DAILYBILLBOARD_DETAILSNEW&columns=SECURITY_CODE,SECUCODE,SECURITY_NAME_ABBR,TRADE_DATE,EXPLAIN,CLOSE_PRICE,CHANGE_RATE,BILLBOARD_NET_AMT,BILLBOARD_BUY_AMT,BILLBOARD_SELL_AMT,BILLBOARD_DEAL_AMT,ACCUM_AMOUNT,DEAL_NET_RATIO,DEAL_AMOUNT_RATIO,TURNOVERRATE,FREE_MARKET_CAP,EXPLANATION,D1_CLOSE_ADJCHRATE,D2_CLOSE_ADJCHRATE,D5_CLOSE_ADJCHRATE,D10_CLOSE_ADJCHRATE,SECURITY_TYPE_CODE&source=WEB&client=WEB&filter=(TRADE_DATE<='{report_date}')(TRADE_DATE>='{report_date}')"

        # 2. 请求数据
        text = requests.request(method="post", url=url).text
        res = json.loads(text[text.index("{") : -2])
        if res["result"] is None:
            return pd.DataFrame()
        df = pd.DataFrame(res["result"]["data"])
        # 3. 解析封装数据
        rename = {
            "SECURITY_CODE": "stock_code",
            "SECURITY_NAME_ABBR": "short_name",
            "TRADE_DATE": "trade_date",
            "CLOSE_PRICE": "close",
            "CHANGE_RATE": "change_cpt",
            "TURNOVERRATE": "turnover_ratio",
            "BILLBOARD_NET_AMT": "a_net_amount",
            "BILLBOARD_BUY_AMT": "a_buy_amount",
            "BILLBOARD_SELL_AMT": "a_sell_amount",
            "BILLBOARD_DEAL_AMT": "a_amount",
            "ACCUM_AMOUNT": "amount",
            "DEAL_NET_RATIO": "net_amount_rate",
            "DEAL_AMOUNT_RATIO": "a_amount_rate",
            "EXPLANATION": "reason",
        }
        df = df.rename(columns=rename)
        df["trade_date"] = pd.to_datetime(df["trade_date"]).dt.strftime("%Y-%m-%d")
        df["short_name"] = df["short_name"].str.replace(" ", "")
        return df[self.__A_LIST_DAILY_COLUMNS]

    def get_a_list_info(self, stock_code, report_date=None):
        """
        获取单个龙虎榜的数据，买5和卖5
        https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123015874658470862357_1721014447038&reportName=RPT_BILLBOARD_DAILYDETAILSBUY&columns=ALL&filter=(TRADE_DATE='2024-07-12')(SECURITY_CODE="600297")&pageNumber=1&pageSize=50&sortTypes=-1&sortColumns=BUY&source=WEB&client=WEB&_=1721014447040
        """
        # 1. url
        urls = [
            f"""https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_BILLBOARD_DAILYDETAILSBUY&columns=ALL&filter=(TRADE_DATE='{report_date}')(SECURITY_CODE="{stock_code}")&pageNumber=1&pageSize=50&sortTypes=-1&sortColumns=BUY&source=WEB&client=WEB&_=1721014447040""",
            f"""https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_BILLBOARD_DAILYDETAILSSELL&columns=ALL&filter=(TRADE_DATE='{report_date}')(SECURITY_CODE="{stock_code}")&pageNumber=1&pageSize=50&sortTypes=-1&sortColumns=BUY&source=WEB&client=WEB&_=1721014447040""",
        ]

        # 2. 请求数据
        data = []
        for url in urls:
            res = requests.request(method="post", url=url).json()
            if res["result"] is None:
                return pd.DataFrame()
            data.extend(res["result"]["data"])
        # ['trade_date', 'stock_code', 'operate_code', 'operate_name', 'buy_amount',
        # 'sell_amount','net_amount', 'buy_amount_rate', 'sell_amount_rate', 'reason']
        # 3. 解析封装数据
        rename = {
            "SECURITY_CODE": "stock_code",
            "TRADE_DATE": "trade_date",
            "OPERATEDEPT_CODE": "operate_code",
            "OPERATEDEPT_NAME": "operate_name",
            "BUY": "a_buy_amount",
            "SELL": "a_sell_amount",
            "NET": "a_net_amount",
            "TOTAL_BUYRIO": "a_buy_amount_rate",
            "TOTAL_SELLRIO": "a_sell_amount_rate",
            "EXPLANATION": "reason",
        }
        df = pd.DataFrame(data).rename(columns=rename)
        df["trade_date"] = pd.to_datetime(df["trade_date"]).dt.strftime("%Y-%m-%d")
        df = df.sort_values(by=["reason", "a_buy_amount", "a_sell_amount"], ascending=[True, False, False])
        return df[self.__A_LIST_INFO_COLUMNS]


if __name__ == "__main__":
    print(AList().list_a_list_daily(report_date="2024-07-04"))
    print(AList().get_a_list_info(stock_code="600297", report_date="2024-07-12"))
