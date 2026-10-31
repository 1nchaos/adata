# -*- coding: utf-8 -*-
"""
http://page3.tdx.com.cn:7615/site/pcwebcall_static/bxb/bxb.html?code=600811&color=1
由xmoney股友提供，感谢支持
@desc: 股票扫雷避险
@author: 1nchaos
@time: 2025/4/2
@log: change log
"""

import pandas as pd
from requests import exceptions as requests_exceptions

from adata._logger import get_logger
from adata.common.utils import requests

logger = get_logger(__name__)


class MineClearance(object):
    __MINE_TDX_COLUMNS = [
        "stock_code",
        "short_name",
        "score",
        "f_type",
        "s_type",
        "t_type",
        "reason",
    ]

    def mine_clearance_tdx(self, stock_code='600811'):
        """
        通达信扫雷信息
        :param stock_code: 股票代码
        :return: 扫雷信息
        """
        url = f"http://page3.tdx.com.cn:7615/site/pcwebcall_static/bxb/json/{stock_code}.json"
        try:
            res = requests.request(method="get", url=url, json={}).json()
            if not isinstance(res, dict):
                raise ValueError(f"返回结构非预期：{type(res).__name__}")
        except (requests_exceptions.RequestException, ValueError, AttributeError):
            # 该代码无扫雷数据或接口不可用时，直接返回“暂无数据”，不再做后续解析
            logger.warning("通达信扫雷数据获取失败，stock_code=%s", stock_code, exc_info=True)
            return pd.DataFrame([{"stock_code": stock_code, "short_name": '', "score": '', "f_type": '暂无数据', }],
                                columns=self.__MINE_TDX_COLUMNS)
        name = res.get("name")
        data = res.get("data")
        data_list = []
        score = 100
        s_type_dict = {}
        for i in data:
            f_type = i.get("name")
            rows = i.get("rows")
            for k in rows:
                if k.get("trigyy"):
                    com_lx = k.get("commonlxid")
                    if len(com_lx) == 0:
                        data_list.append({
                            "stock_code": stock_code,
                            "short_name": name,
                            "f_type": f_type,
                            "s_type": k.get("lx"),
                            "t_type": '',
                            "reason": k.get("trigyy"),
                            "score": k.get("fs"),
                        })
                        if k.get("trig") == 1:
                            score = score - k.get('fs')
                    for j in com_lx:
                        if j.get("trigyy"):
                            data_list.append({
                                "stock_code": stock_code,
                                "short_name": name,
                                "f_type": f_type,
                                "s_type": k.get("lx"),
                                "t_type": j.get("lx"),
                                "reason": j.get("trigyy"),
                                "score": j.get("fs"),
                            })
                            if j.get("trig") == 1 and not s_type_dict.get(k.get("lx")):
                                score = score - j.get('fs')
                                s_type_dict[k.get("lx")] = j.get("fs")
        # 清洗数据
        res = pd.DataFrame(data_list, columns=self.__MINE_TDX_COLUMNS)
        score = score if score > 1 else 1
        res["score"] = score
        if len(res) == 0:
            if name.endswith("退"):
                res = pd.DataFrame([{"stock_code": stock_code, "short_name": name, "score": -1, "f_type": '已退市', }],
                                   columns=self.__MINE_TDX_COLUMNS)
            else:
                res = pd.DataFrame(
                    [{"stock_code": stock_code, "short_name": name, "score": score, "f_type": '暂无风险项', }],
                    columns=self.__MINE_TDX_COLUMNS)
        return res


if __name__ == '__main__':
    mine_clearance = MineClearance()
    print(mine_clearance.mine_clearance_tdx("600074"))
