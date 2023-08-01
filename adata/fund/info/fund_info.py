# -*- coding: utf-8 -*-
"""
@desc: 基金信息 etf

http://quote.eastmoney.com/center/gridlist.html#fund_etf

@author: 1nchaos
@time: 2023/5/31
@log: change log
"""
import copy
import math

import pandas as pd

from adata.common import requests
from adata.common.headers import ths_headers


class FundInfo(object):
    """
    基金信息
    """
    __ETF_INFO_COLUMNS = ['fund_code', 'short_name', 'net_value', 'net_date', 'exchange']

    def __init__(self) -> None:
        super().__init__()

    def all_etf_exchange_traded_info(self):
        """
        获取所有etl（场内）的信息
        :return: ['fund_code', 'short_name', 'net_value', 'net_date', 'exchange']
        fund_code: 基金代码
        short_name: 简称
        net_value: 净值
        net_date: 净值日期
        exchange: 交易所，SZ，SH
        """
        return self.__all_etf_exchange_traded_info_ths()

    def __all_etf_exchange_traded_info_ths(self):
        """
        http://www.iwencai.com/gateway/urp/v7/landing/getDataList?query=基金市场类型包含ETF(场内)&perpage=100&page=1&query_type=fund&comp_id=6757566&uuid=24088
        :return:
        """
        # 1. url拼接页码等参数
        data = []
        total_pages = 1
        curr_page = 1
        while curr_page <= total_pages:
            api_url = f"http://www.iwencai.com/gateway/urp/v7/landing/getDataList?query=基金市场类型包含ETF(场内)" \
                      f"&perpage=100&page={curr_page}&query_type=fund&comp_id=6757566&uuid=24088"
            headers = copy.deepcopy(ths_headers.json_headers)
            headers['Host'] = 'www.iwencai.com'
            headers['Sec-Fetch-Mode'] = 'navigate'
            res = requests.request(method='get', url=api_url, headers=headers, proxies={})
            curr_page += 1
            # 2. 判断请求是否成功
            if res.status_code != 200:
                continue
            text = res.text.encode('utf-8').decode('unicode escape')
            if 'ETF(场内)' not in text:
                break
            res_json = res.json()
            data_dic = res_json['answer']['components'][0]['data']
            # 3 .获取总的页数
            if total_pages == 1:
                total_pages = math.ceil(data_dic['meta']['extra']['code_count'] / 100)
            # 4. 解析数据
            page_data = []
            data_list = data_dic['datas']
            for one in data_list:
                if 'ETF(场内)' in one['基金@基金市场类型']:
                    page_data.append({'fund_code': one['code'], 'short_name': one['基金简称'],
                                      'net_value': one['基金@最新单位净值'], 'net_date': one['基金@最新净值日期'],
                                      'exchange': one['基金代码'].split('.')[1]})
            data.extend(page_data)
            # 5. 封装数据
            if not data:
                return pd.DataFrame(data=data, columns=self.__ETF_INFO_COLUMNS)
        result_df = pd.DataFrame(data=data)
        data.clear()
        return result_df[self.__ETF_INFO_COLUMNS]


if __name__ == '__main__':
    print(FundInfo().all_etf_exchange_traded_info())
