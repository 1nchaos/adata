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
        text = requests.request(method='post', url=url).text
        res = json.loads(text[text.index('{'):-2])
        df = pd.DataFrame(res['result']["data"])

        # 3. 解析封装数据 TODO
        rename = {'f2': 'price', 'f3': 'change_pct', 'f12': 'stock_code', 'f14': 'short_name', }
        rank_df = pd.rename(columns=rename)
        rank_df["change_pct"] = pd.to_numeric(rank_df["change_pct"], errors="coerce")
        rank_df["price"] = pd.to_numeric(rank_df["price"], errors="coerce")
        rank_df["change"] = rank_df["price"] * rank_df["change_pct"] / 100
        rank_df["rank"] = range(1, len(rank_df) + 1)
        return rank_df[["rank", "stock_code", "short_name", "price", "change", "change_pct"]]

    def get_a_list(self, stock_code, report_date=None):
        """
        获取单个龙虎榜的数据，买5和卖5
        https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112307421020653512591_1716975849191&reportName=RPT_BILLBOARD_DAILYDETAILSBUY&columns=ALL&filter=(TRADE_DATE%3D%272024-05-21%27)(SECURITY_CODE%3D%22000070%22)&pageNumber=1&pageSize=50&sortTypes=-1&sortColumns=BUY&source=WEB&client=WEB&_=1716975849193
        https://data.eastmoney.com/stock/tradedetail.html
        """
        pass


if __name__ == '__main__':
    AList().list_a_list_daily()
