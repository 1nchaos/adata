# -*- coding: utf-8 -*-
"""
@desc: 热点榜单 TODO

同花顺热点榜单
https://eq.10jqka.com.cn/frontend/thsTopRank/index.html?fontzoom=no&client_userid=ceZLR&share_hxapp=gsc&share_action=webpage_share.hot_list_1714369375634&back_source=wxhy#/

@author: 1nchaos
@time: 2024/4/29
@log: change log
"""
import pandas as pd

from adata.common.base.base_ths import BaseThs
from adata.common.headers import ths_headers
from adata.common.utils import requests


class Hot(BaseThs):
    """热门榜单"""

    # 东方财富人气榜
    def pop_rank_100_east(self):
        """
        东方财富人气榜100
        http://guba.eastmoney.com/rank/
        """
        # 1.url
        url = "https://emappdata.eastmoney.com/stockrank/getAllCurrentList"

        # 2. 请求数据
        params = {"appId": "appId01", "globalId": "786e4c21-70dc-435a-93bb-38",
                  "marketType": "", "pageNo": 1, "pageSize": 100, }
        res = requests.request(method='post', url=url, json=params).json()
        df = pd.DataFrame(res["data"])

        df["mark"] = ["0" + "." + item[2:] if "SZ" in item else "1" + "." + item[2:]
                      for item in df["sc"]]
        ",".join(df["mark"]) + "?v=08926209912590994"
        params = {"ut": "f057cbcbce2a86e2866ab8877db1d059",
                  "fltt": "2", "invt": "2", "fields": "f14,f3,f12,f2",
                  "secids": ",".join(df["mark"]) + ",?v=08926209912590994", }
        url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
        res = requests.request(method='get', url=url, params=params)

        # 3. 解析封装数据
        data = res.json()["data"]["diff"]
        rename = {'f2': 'price', 'f3': 'change_pct', 'f12': 'stock_code', 'f14': 'short_name', }
        rank_df = pd.DataFrame(data).rename(columns=rename)
        rank_df["change_pct"] = pd.to_numeric(rank_df["change_pct"], errors="coerce")
        rank_df["price"] = pd.to_numeric(rank_df["price"], errors="coerce")
        rank_df["change"] = rank_df["price"] * rank_df["change_pct"] / 100
        rank_df["rank"] = range(1, len(rank_df) + 1)
        return rank_df[["rank", "stock_code", "short_name", "price", "change", "change_pct"]]

    def hot_rank_100_ths(self):
        """
        同花顺热股100
        https://dq.10jqka.com.cn/fuyao/hot_list_data/out/hot_list/v1/stock?stock_type=a&type=hour&list_type=normal
        """
        api_url = 'https://dq.10jqka.com.cn/fuyao/hot_list_data/out/hot_list/v1/stock?stock_type=a&type=hour&list_type=normal'
        headers = ths_headers.json_headers
        headers['Host'] = 'dq.10jqka.com.cn'
        res = requests.request(method='get', url=api_url, params={}, headers=headers)
        data = res.json()['data']['stock_list']
        data_list = []
        for d in data:
            d['concept_tag'] = ";".join(d['tag']['concept_tag'])
            if 'popularity_tag' in d['tag']:
                d['pop_tag'] = d['tag']['popularity_tag'].replace('\n', '')
            data_list.append(d)
        rename = {'order': 'rank', 'rise_and_fall': 'change_pct', 'code': 'stock_code', 'name': 'short_name',
                  'rate': 'hot_value', 'concept_tag': 'concept_tag'}
        rank_df = pd.DataFrame(data).rename(columns=rename)
        rank_df = rank_df[["rank", "stock_code", "short_name", "change_pct", "hot_value", "pop_tag", "concept_tag"]]
        return rank_df

    def hot_concept_20_ths(self, plate_type=1):
        """
        同花热门概念板块
        :param plate_type: 1.概念板块，2.行业板块；默认：概念板块
        """
        plate_type = 'concept' if plate_type == 1 else 'industry'
        api_url = f'https://dq.10jqka.com.cn/fuyao/hot_list_data/out/hot_list/v1/plate?type={plate_type}'
        headers = ths_headers.json_headers
        headers['Host'] = 'dq.10jqka.com.cn'
        res = requests.request(method='get', url=api_url, params={}, headers=headers)
        data = res.json()['data']['plate_list']
        data_list = []
        for d in data:
            data_list.append(d)
        rename = {'order': 'rank', 'rise_and_fall': 'change_pct', 'rate': 'hot_value', 'code': 'concept_code',
                  'name': 'concept_name'}
        rank_df = pd.DataFrame(data).rename(columns=rename)
        rank_df = rank_df[["rank", "concept_code", "concept_name", "change_pct", "hot_value", "hot_tag"]]
        return rank_df


if __name__ == '__main__':
    print(Hot().hot_rank_100_ths())
    print(Hot().pop_rank_100_east())
    print(Hot().hot_concept_20_ths(plate_type=1))
    print(Hot().hot_concept_20_ths(plate_type=2))
