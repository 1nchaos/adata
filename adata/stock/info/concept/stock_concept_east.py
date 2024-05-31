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

import pandas as pd

from adata.common import requests
from adata.common.utils.code_utils import compile_exchange_by_stock_code
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
        url = (
            "https://push2.eastmoney.com/api/qt/clist/get"
            "?pn=1&pz=1000&po=1&np=1&fields=f12%2Cf13%2Cf14%2Cf62&fid=f62&fs=m%3A90%2Bt%3A3"
        )
        res_json = requests.request("get", url, headers={}, proxies={}).json()
        res_data = res_json["data"]["diff"]
        data = []
        for _ in res_data:
            data.append(
                {
                    "index_code": _["f12"],
                    "concept_code": _["f12"],
                    "name": _["f14"],
                    "source": "东方财富",
                }
            )
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
            url = (
                f"https://push2.eastmoney.com/api/qt/clist/get"
                f"?fid=f62&po=1&pz=1000&pn={curr_page}&np=1&fltt=2&invt=2&fs=b:{concept_code}&fields=f12,f14"
            )
            res_json = requests.request(
                "get", url, headers={}, proxies={}, wait_time=wait_time
            ).json()
            res_data = res_json["data"]
            if not res_data:
                break
            res_data = res_data["diff"]
            for _ in res_data:
                data.append({"stock_code": _["f12"], "short_name": _["f14"]})
            curr_page += 1
        result_df = pd.DataFrame(data=data, columns=self._CONCEPT_CONSTITUENT_COLUMNS)
        return result_df

    def get_concept_east(self, stock_code: str = "000001"):
        """
        根据股票代码获取，股票所属的所有的概念信息
        https://datacenter.eastmoney.com/securities/api/data/v1/get?
        reportName=RPT_F10_CORETHEME_BOARDTYPE
        &columns=SECUCODE%2CSECURITY_CODE%2CSECURITY_NAME_ABBR%2CNEW_BOARD_CODE%2CBOARD_NAME%2CSELECTED_BOARD_REASON%2CIS_PRECISE%2CBOARD_RANK%2CBOARD_YIELD%2CDERIVE_BOARD_CODE
        &quoteColumns=f3~05~NEW_BOARD_CODE~BOARD_YIELD
        &filter=(SECUCODE%3D%22600138.SH%22)(IS_PRECISE%3D%221%22)
        &pageNumber=1&pageSize=&sortTypes=1&sortColumns=BOARD_RANK&source=HSF10&client=PC&v=0029565688091059528
        :param stock_code: 股票代码
        :return: 概念信息
        """
        stock_code = compile_exchange_by_stock_code(stock_code)
        url = (
            f"https://datacenter.eastmoney.com/securities/api/data/v1/get?"
            f"reportName=RPT_F10_CORETHEME_BOARDTYPE&"
            f"columns=SECUCODE%2CSECURITY_CODE%2CSECURITY_NAME_ABBR%2CNEW_BOARD_CODE%2CBOARD_NAME%2CSELECTED_BOARD_REASON%2CIS_PRECISE%2CBOARD_RANK%2CBOARD_YIELD%2CDERIVE_BOARD_CODE&"
            f"quoteColumns=f3~05~NEW_BOARD_CODE~BOARD_YIELD&"
            f"filter=(SECUCODE%3D%22{stock_code}%22)(IS_PRECISE%3D%221%22)&pageNumber=1&pageSize=50&sortTypes=1&"
            f"sortColumns=BOARD_RANK&source=HSF10&client=PC"
        )
        res_json = requests.request("get", url, headers={}, proxies={}).json()
        # 1. 返回结果判断
        if not res_json["success"]:
            return pd.DataFrame(data=[], columns=self._CONCEPT_INFO_COLUMNS)

        # 2. 正常返回数据结果封装
        res_data = res_json["result"]["data"]
        data = []
        for _ in res_data:
            # ['stock_code', 'short_name', 'concept_code', 'name', 'reason', 'source']
            data.append(
                {
                    "stock_code": _["SECURITY_CODE"],
                    "concept_code": _["NEW_BOARD_CODE"],
                    "name": _["BOARD_NAME"],
                    "reason": _["SELECTED_BOARD_REASON"],
                    "source": "东方财富",
                }
            )
        result_df = pd.DataFrame(data=data, columns=self._CONCEPT_INFO_COLUMNS)
        return result_df

    def get_board_east(self, stock_code: str = "000001") -> pd.DataFrame:
        """
        根据股票代码获取，股票所属的板块+板块类型信息
        :param stock_code: 股票代码
        :return: 概念信息
        """
        stock_code = compile_exchange_by_stock_code(stock_code)
        url = (
            f"https://datacenter.eastmoney.com/securities/api/data/get?"
            f"type=RPT_F10_CORETHEME_BOARDTYPE&"
            f"sty=SECUCODE%2CSECURITY_CODE%2CSECURITY_NAME_ABBR%2CBOARD_CODE%2CBOARD_NAME%2CIS_PRECISE%2CBOARD_RANK%2CBOARD_TYPE&"
            f"filter=(SECUCODE%3D%22{stock_code}%22)&"
            f"p=1&ps=&sr=1&st=BOARD_RANK&source=HSF10&client=PC"
        )

        res_json = requests.request("get", url, headers={}, proxies={}).json()
        # 1. 返回结果判断
        if not res_json["success"]:
            return pd.DataFrame(data=[], columns=self._CONCEPT_INFO_COLUMNS)

        # 2. 正常返回数据结果封装
        res_data = res_json["result"]["data"]
        data = []
        # BOARD_TYPE: 行业/板块/题材
        for _ in res_data:
            data.append(
                {
                    "stock_code": _["SECURITY_CODE"],
                    "board_type": _["BOARD_TYPE"] if _["BOARD_TYPE"] else "题材",
                    "board_name": _["BOARD_NAME"],
                    "source": "东方财富",
                }
            )

        result_df = pd.DataFrame(data=data, columns=self._BOARD_INFO_COLUMNS)
        return result_df


if __name__ == "__main__":
    print(StockConceptEast().all_concept_code_east())
    print(StockConceptEast().concept_constituent_east(concept_code="BK0637"))
    print(StockConceptEast().get_concept_east(stock_code="600020").to_string())
    print(StockConceptEast().get_board_east(stock_code="603177").to_string())
