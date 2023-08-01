# -*- coding: utf-8 -*-
"""
@desc: 基金信息 etf

http://quote.eastmoney.com/center/gridlist.html#fund_etf

@author: 1nchaos
@time: 2023/5/31
@log: change log
"""
import json
import math

import pandas as pd

from adata.common import requests
from adata.common.base.base_ths import BaseThs
from adata.common.exception.exception_msg import THS_IP_LIMIT_RES, THS_IP_LIMIT_MSG


class FundInfo(BaseThs):
    """
    基金信息
    """
    __ETF_INFO_COLUMNS = ['fund_code', 'short_name', 'net_value']

    def __init__(self) -> None:
        super().__init__()

    def all_etf_exchange_traded_info(self, wait_time=None):
        """
        获取所有etl（场内）的信息
        :return: ['fund_code', 'short_name', 'net_value']
        fund_code: 基金代码
        short_name: 简称
        net_value: 最新净值
        """
        return self.__all_etf_exchange_traded_info_east(wait_time=wait_time)

    def __all_etf_exchange_traded_info_ths(self, wait_time):
        """
        http://www.iwencai.com/customized/chart/get-robot-data
        """
        wc_url = 'http://www.iwencai.com/customized/chart/get-robot-data'
        # 1. url拼接页码等参数
        data = []
        total_pages = 1
        curr_page = 1
        while curr_page <= total_pages:
            params = {'source': "Ths_iwencai_Xuangu", 'version': '2.0', 'query_area': '', 'block_list': '',
                      'add_info': '{\"urp\":{\"scene\":1,\"company\":1,\"business\":1},\"contentType\":\"json\",\"searchInfo\":true}',
                      'question': '基金市场类型包含ETF(场内)', 'perpage': 100, 'page': curr_page, 'secondary_intent': 'fund',
                      'log_info': '{\"input_type\":\"typewrite\"}',
                      'rsh': 'Ths_iwencai_Xuangu_kn63wc5it6hwdapiye6hplx8h86di15p'}

            headers = {'Host': 'www.iwencai.com', 'Content-Type': 'application/json',
                       'Origin': 'http://www.iwencai.com',
                       'Accept': 'application/json, text/plain, */*', 'hexin-v': self.wencai_hexin_v()}
            res = requests.request(method='post', url=wc_url, headers=headers, data=json.dumps(params),
                                   wait_time=wait_time)
            curr_page += 1
            # 2. 判断请求是否成功
            if res.status_code != 200:
                continue
            text = res.text.encode('utf-8').decode('unicode escape')
            if THS_IP_LIMIT_RES in text:
                return Exception(THS_IP_LIMIT_MSG)
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
        result_df = pd.DataFrame(data=data, columns=self.__ETF_INFO_COLUMNS)
        data.clear()
        return result_df[self.__ETF_INFO_COLUMNS]

    def __all_etf_exchange_traded_info_east(self, wait_time):
        """
        http://68.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124047482019788167995_1690884441114&pn=1&pz=500&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=b:MK0021,b:MK0022,b:MK0023,b:MK0024&fields=f12,f14,f2&_=1690884441121
        :param wait_time: 等待时间
        :return:
        """
        curr_page = 1
        data = []
        while curr_page < 5:
            url = f"http://68.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124047482019788167995_1690884441114" \
                  f"&pn={curr_page}&pz=500&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web" \
                  f"&fid=f3&fs=b:MK0021,b:MK0022,b:MK0023,b:MK0024&fields=f12,f14,f2&_=1690884441121"
            text = requests.request('get', url, headers={}, proxies={}, wait_time=wait_time).text
            res_json = json.loads(text[text.index('{'):-2])
            res_data = res_json['data']
            if not res_data:
                break
            res_data = res_data['diff']
            for _ in res_data:
                data.append({'fund_code': _['f12'], 'short_name': _['f14'], 'net_value': _['f2']})
            curr_page += 1
        result_df = pd.DataFrame(data=data, columns=self.__ETF_INFO_COLUMNS)
        return result_df


if __name__ == '__main__':
    print(FundInfo().all_etf_exchange_traded_info())
