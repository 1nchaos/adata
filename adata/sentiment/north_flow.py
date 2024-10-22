# -*- coding: utf-8 -*-
"""
@desc:
北向资金
来源：东方财富
https://data.eastmoney.com/hsgt/index.html
https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112307442704592215257_1690813516314&sortColumns=TRADE_DATE&sortTypes=-1&pageSize=10&pageNumber=2&reportName=RPT_MUTUAL_DEAL_HISTORY&columns=ALL&source=WEB&client=WEB&filter=(MUTUAL_TYPE="001")
同花顺
https://data.hexin.cn/market/hsgtApi/method/hsgtData/

@author: 1nchaos
@time: 2023/7/28
@log: change log
"""
import copy
import datetime
import json
import math

import pandas as pd

from adata.common import requests
from adata.common.base.base_ths import BaseThs
from adata.common.exception.exception_msg import THS_IP_LIMIT_RES, THS_IP_LIMIT_MSG
from adata.common.headers import ths_headers


class NorthFlow(BaseThs):
    __NORTH_FLOW_COLUMNS = [
        "trade_date",
        "net_hgt",
        "buy_hgt",
        "sell_hgt",
        "net_sgt",
        "buy_sgt",
        "sell_sgt",
        "net_tgt",
        "buy_tgt",
        "sell_tgt",
    ]

    __NORTH_FLOW_MIN_COLUMNS = ["trade_time", "net_hgt", "net_sgt", "net_tgt"]
    __NORTH_FLOW_CURRENT_COLUMNS = __NORTH_FLOW_MIN_COLUMNS

    def __init__(self) -> None:
        super().__init__()

    def north_flow(self, start_date=None):
        """
        获取北向资金历史的数据，开始时间到最新的历史数据，
        :param start_date: 开始时间，最早：1017-01-01
        :return:
        'trade_date'：交易日期
        'net_hgt', ：沪港通净买入金额（元）
        'buy_hgt', ：沪港通净买入金额（元）
        'sell_hgt', ：沪港通净买入金额（元）
        'net_sgt', ：深港通净买入金额（元）
        'buy_sgt', ：深港通净买入金额（元）
        'sell_sgt', ：深港通卖出金额（元）
        'net_tgt', ：合计净买入金额（元）
        'buy_tgt', ：合计买入金额（元）
        'sell_tgt' ：合计卖出金额（元）
        """

        return self.__north_flow_east(start_date=start_date)

    def __north_flow_east(self, start_date=None):
        """
        https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112307442704592215257_1690813516314&sortColumns=TRADE_DATE&sortTypes=-1&pageSize=10&pageNumber=2&reportName=RPT_MUTUAL_DEAL_HISTORY&columns=ALL&source=WEB&client=WEB&filter=(MUTUAL_TYPE="001")
        """
        if start_date:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            date_min = datetime.datetime.strptime("2017-01-01", "%Y-%m-%d")
            if start_date < date_min:
                start_date = date_min
        curr_page = 1
        data = []
        while curr_page < 18:
            url = (
                f"https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112307442704592215257_1690813516314"
                f"&sortColumns=TRADE_DATE&sortTypes=-1&pageSize=1000&pageNumber={curr_page}&"
                f"reportName=RPT_MUTUAL_DEAL_HISTORY&columns=ALL&source=WEB&client=WEB&"
            )
            sgt_url = f"""{url}filter=(MUTUAL_TYPE="001")"""
            hgt_url = f"""{url}filter=(MUTUAL_TYPE="003")"""

            sgt = requests.request("get", sgt_url, headers={}, proxies={}).text.replace("null", "0")
            hgt = requests.request("get", hgt_url, headers={}, proxies={}).text.replace("null", "0")

            # 2. 解析数据
            sgt_json = json.loads(sgt[sgt.index("{") : -2])
            hgt_json = json.loads(hgt[hgt.index("{") : -2])
            sgt_data = sgt_json["result"]["data"]
            hgt_data = hgt_json["result"]["data"]
            if not sgt_data:
                break
            is_end = False
            for i in range(len(sgt_data)):
                if not start_date and i >= 30:
                    is_end = True
                    break
                if start_date:
                    date_min = datetime.datetime.strptime(hgt_data[i]["TRADE_DATE"], "%Y-%m-%d %H:%M:%S")
                    if start_date > date_min:
                        is_end = True
                        break

                data.append(
                    {
                        "trade_date": hgt_data[i]["TRADE_DATE"],
                        "net_hgt": math.ceil(hgt_data[i]["NET_DEAL_AMT"] * 1000000),
                        "buy_hgt": math.ceil(hgt_data[i]["BUY_AMT"] * 1000000),
                        "sell_hgt": math.ceil(hgt_data[i]["SELL_AMT"] * 1000000),
                        "net_sgt": math.ceil(sgt_data[i]["NET_DEAL_AMT"] * 1000000),
                        "buy_sgt": math.ceil(sgt_data[i]["BUY_AMT"] * 1000000),
                        "sell_sgt": math.ceil(sgt_data[i]["SELL_AMT"] * 1000000),
                        "net_tgt": math.ceil((hgt_data[i]["NET_DEAL_AMT"] + sgt_data[i]["NET_DEAL_AMT"]) * 1000000),
                        "buy_tgt": math.ceil((hgt_data[i]["BUY_AMT"] + sgt_data[i]["BUY_AMT"]) * 1000000),
                        "sell_tgt": math.ceil((hgt_data[i]["SELL_AMT"] + sgt_data[i]["SELL_AMT"]) * 1000000),
                    }
                )

            if is_end:
                break
            curr_page += 1

        # 3.封装数据
        result_df = pd.DataFrame(data=data, columns=self.__NORTH_FLOW_COLUMNS)
        result_df["trade_date"] = pd.to_datetime(result_df["trade_date"]).dt.strftime("%Y-%m-%d")

        return result_df[self.__NORTH_FLOW_COLUMNS]

    def north_flow_min(self):
        """
        获取北向的分时数据，最新交易日的
        https://data.hexin.cn/market/hsgtApi/method/dayChart/
        """
        res = self.__north_flow_min_east()
        # res = pd.DataFrame()
        if res.empty:
            res = self.__north_flow_min_ths()
        return res

    def north_flow_current(self):
        """
        获取北向的最新数据，最新交易日的
        """
        return self.north_flow_min().tail(1)

    def __north_flow_min_ths(self):
        # 1.接口 url
        api_url = f" https://data.hexin.cn/market/hsgtApi/method/dayChart/"
        headers = copy.deepcopy(ths_headers.json_headers)
        headers["Host"] = "data.hexin.cn"
        res = requests.request("get", api_url, headers=headers, proxies={})
        text = res.text
        if THS_IP_LIMIT_RES in text:
            return Exception(THS_IP_LIMIT_MSG)
        if not text:
            return pd.DataFrame(data=[], columns=self.__NORTH_FLOW_CURRENT_COLUMNS)
        # 2. 解析数据
        result_json = json.loads(text)
        time_list = result_json["time"]
        hgt_list = result_json["hgt"]
        sgt_list = result_json["sgt"]
        data = []
        for i in range(len(time_list)):
            row = [
                time_list[i],
                math.ceil(hgt_list[i] * 100000000),
                math.ceil(sgt_list[i] * 100000000),
                math.ceil((hgt_list[i] + sgt_list[i]) * 100000000),
            ]
            data.append(row)
        # 3. 封装数据
        result_df = pd.DataFrame(data=data, columns=self.__NORTH_FLOW_MIN_COLUMNS)
        import adata

        trade_year = adata.stock.info.trade_calendar()
        # 获取当前日期
        today = datetime.datetime.today().date()
        # 筛选出小于等于今天并且 trade_status=1 的记录
        trade_year["trade_date"] = pd.to_datetime(trade_year["trade_date"])
        filtered_df = trade_year[(trade_year["trade_date"].dt.date <= today) & (trade_year["trade_status"] == 1)]
        max_date = filtered_df.loc[filtered_df["trade_date"].idxmax()]

        result_df["trade_time"] = max_date["trade_date"].strftime("%Y-%m-%d") + " " + result_df["trade_time"]

        # 将 trade_time 字符串转换为日期时间类型
        result_df["trade_time"] = pd.to_datetime(result_df["trade_time"])
        return result_df[self.__NORTH_FLOW_MIN_COLUMNS]

    def __north_flow_min_east(self):
        """
        https://push2.eastmoney.com/api/qt/kamt.rtmin/get?fields1=f1,f3&fields2=f51,f52,f54,f56&ut=b2884a393a59ad64002292a3e90d46a5&cb=jQuery1123041654203412972746_1690859251791&_=1690859251792
        :return:
        """
        # 1. 请求数据
        url = "https://push2.eastmoney.com/api/qt/kamt.rtmin/get?fields1=f1,f3&fields2=f51,f52,f54,f56&ut=b2884a393a59ad64002292a3e90d46a5&cb=jQuery112308613678156517719_1690861908580&_=1690861908581"
        data = []
        try:
            gt = requests.request("get", url, headers={}, proxies={}).text

            # 2. 解析数据
            gt_json = json.loads(gt[gt.index("{") : -2])
            gt_date = gt_json["data"]["s2nDate"]
            gt_data = gt_json["data"]["s2n"]
            for _ in gt_data:
                row = str(_).split(",")
                if row[1] != "-":
                    data.append(
                        [
                            row[0],
                            math.ceil(float(row[1]) * 10000),
                            math.ceil(float(row[2]) * 10000),
                            math.ceil(float(row[3]) * 10000),
                        ]
                    )
        except Exception as e:
            print("north_flow_min_east is ERROR!!!")
            return pd.DataFrame(data=data, columns=self.__NORTH_FLOW_MIN_COLUMNS)
        result_df = pd.DataFrame(data=data, columns=self.__NORTH_FLOW_MIN_COLUMNS)

        # 3. 封装数据
        result_df["trade_time"] = str(datetime.datetime.now().year) + "-" + gt_date + " " + result_df["trade_time"]
        result_df["trade_time"] = pd.to_datetime(result_df["trade_time"])
        result_df = result_df.dropna()
        return result_df[self.__NORTH_FLOW_MIN_COLUMNS]


if __name__ == "__main__":
    print(NorthFlow().north_flow_min())
    print(NorthFlow().north_flow_current())
    print(NorthFlow().north_flow(start_date="2000-11-01"))
