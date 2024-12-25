# -*- coding: utf-8 -*-
"""
@desc: 股票资金流向

东方财富：个股
https://data.eastmoney.com/zjlx/000001.html
https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?cb=jQuery112303663243111530894_1718714074308&lmt=0&klt=101&fields1=f1%2Cf2%2Cf3%2Cf7&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61%2Cf62%2Cf63%2Cf64%2Cf65&ut=b2884a393a59ad64002292a3e90d46a5&secid=1.600519&_=1718714074309

@author: 1nchaos
@time: 2024/6/7
@log: change log
"""
import json

import pandas as pd

from adata.common.utils import requests


class CapitalFlowEast(object):
    _FLOW_COLUMNS = ['index_code', 'index_name', 'change_pct', 'main_net_inflow', 'main_net_inflow_rate',
                     'max_net_inflow', 'max_net_inflow_rate', 'lg_net_inflow', 'lg_net_inflow_rate',
                     'mid_net_inflow', 'mid_net_inflow_rate', 'sm_net_inflow', 'sm_net_inflow_rate',
                     'stock_code', 'stock_name']

    def all_capital_flow_east(self, days_type=1):
        """
        获取
        :param days_type: 天数类型：1.当天，5.最近5日；10.最近十日
        :return: 概念资金流向
        """
        # 1. 请求接口 url
        fid = {
            1: 'f62',
            5: 'f164',
            10: 'f174'
        }.get(days_type, 'f62')
        fields = {
            1: 'f12,f14,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205',
            5: 'f12,f14,f109,f164,f165,f166,f167,f168,f169,f170,f171,f172,f173,f257,f258',
            10: 'f12,f14,f160,f174,f175,f176,f177,f178,f179,f180,f181,f182,f183,f260,f261'
        }.get(days_type, 'f62')
        url = f"https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112309367957412610306_1735123926723&fid={fid}&po=1&pz=1000&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m:90 t:3&fields={fields}"
        res = requests.request(method='get', url=url, headers={})
        text = res.text
        text = text[text.index('(') + 1:-2]
        data = json.loads(text)['data']

        # 2. 解析数据
        if not data:
            return pd.DataFrame([], columns=self._FLOW_COLUMNS)
        data = data['diff']
        data_list = []
        fields = fields.split(',')
        for item in data:
            dt = {}
            for i in range(len(self._FLOW_COLUMNS)):
                if item[fields[i]] == '-':
                    continue
                dt[self._FLOW_COLUMNS[i]] = item[fields[i]]
            if len(dt) == len(self._FLOW_COLUMNS):
                data_list.append(dt)
        # 3. 数据etl
        df = pd.DataFrame(data_list, columns=self._FLOW_COLUMNS)
        df = df.astype({'change_pct': 'float64', 'main_net_inflow': 'float64', 'sm_net_inflow': 'float64',
                        'mid_net_inflow': 'float64', 'lg_net_inflow': 'float64', 'max_net_inflow': 'float64',
                        'main_net_inflow_rate': 'float64', 'sm_net_inflow_rate': 'float64',
                        'mid_net_inflow_rate': 'float64', 'lg_net_inflow_rate': 'float64',
                        'max_net_inflow_rate': 'float64'
                        })
        return df


if __name__ == '__main__':
    print(CapitalFlowEast().all_capital_flow_east(days_type=10))
