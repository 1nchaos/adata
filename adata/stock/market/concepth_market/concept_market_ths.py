# -*- coding: utf-8 -*-
"""
@summary: 股票概念 行情
同花顺概念更及时和完整，所以目前暂只基于同花顺的股票概念抓取,网页数据中心和手机概念板块
http://d.10jqka.com.cn/v6/line/48_885772/01/last1800.js
http://search.10jqka.com.cn/gateway/urp/v7/landing/getDataList?query=%E6%89%80%E6%9C%89%E6%A6%82%E5%BF%B5&condition=%5B%7B%22indexName%22%3A%22%E6%8C%87%E6%95%B0%40%E5%90%8C%E8%8A%B1%E9%A1%BA%E6%A6%82%E5%BF%B5%E6%8C%87%E6%95%B0%22%2C%22indexProperties%22%3A%5B%5D%2C%22source%22%3A%22new_parser%22%2C%22type%22%3A%22index%22%2C%22indexPropertiesMap%22%3A%7B%7D%2C%22reportType%22%3A%22null%22%2C%22chunkedResult%22%3A%22%E6%89%80%E6%9C%89%E6%A6%82%E5%BF%B5%22%2C%22valueType%22%3A%22_%E6%8C%87%E6%95%B0%E7%B1%BB%E5%9E%8B%22%2C%22domain%22%3A%22abs_a%E6%8C%87%E9%A2%86%E5%9F%9F%22%2C%22uiText%22%3A%22%E5%90%8C%E8%8A%B1%E9%A1%BA%E6%A6%82%E5%BF%B5%E6%8C%87%E6%95%B0%22%2C%22sonSize%22%3A0%2C%22queryText%22%3A%22%E5%90%8C%E8%8A%B1%E9%A1%BA%E6%A6%82%E5%BF%B5%E6%8C%87%E6%95%B0%22%2C%22relatedSize%22%3A0%7D%5D&urp_sort_index=%E6%8C%87%E6%95%B0%E4%BB%A3%E7%A0%81&source=Ths_iwencai_Xuangu&perpage=500&page=1&urp_sort_way=desc&codelist=&page_id=&logid=35df00ee5ae706d0dfcd0dbfdb846e0c&ret=json_all&sessionid=35df00ee5ae706d0dfcd0dbfdb846e0c&iwc_token=0ac9667016801698001765831&user_id=Ths_iwencai_Xuangu_7fahywzhbkrh4lwwkwfw936njqbjzsly&uuids%5B0%5D=23119&query_type=zhishu&comp_id=6367801&business_cat=soniu&uuid=23119
885772 表示同花顺的概念指数的代码
@author: 1nchaos
@date: 2023/3/30 16:17
"""
import copy
import json

import numpy as np
import pandas as pd

from adata.common.base.base_ths import BaseThs
from adata.common.exception.exception_msg import *
from adata.common.headers import ths_headers


class ConceptMarketThs(BaseThs):
    """
    股票概念 行情
    """
    __MARKET_COLUMNS = ['index_code', 'trade_time', 'trade_date', 'open', 'high', 'low', 'close', 'volume',
                        'amount', 'change', 'change_pct']
    __MARKET_CONCEPT_MIN_COLUMNS = ['index_code', 'trade_time', 'trade_date', 'price', 'avg_price', 'volume',
                                    'amount', 'change', 'change_pct']
    __MARKET_CONCEPT_CURRENT_COLUMNS = ['index_code', 'trade_time', 'trade_date', 'open', 'high', 'low', 'price',
                                        'volume', 'amount']

    def get_market_concept_ths(self, index_code: str = '886013', k_type: int = 1, adjust_type: int = 1):
        """
        获取同花顺的概念的行情
        web: http://q.10jqka.com.cn/gn/
        pc: http://d.10jqka.com.cn/v4/line/bk_885772/21/last.js
        app: http://d.10jqka.com.cn/v6/line/48_886013/01/last1800.js
        00 日k不复权；01日k前复权；02日k后复权；11周k前复权；21月k前复权
        :param index_code: 同花顺概念指数代码
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :param adjust_type: k线复权类型：0.不复权；1.前复权；2.后复权 默认：1 前复权
        :return: k线行情数据 [日期，开，高，低，收,成交量，成交额]
        ;20230419,958.901,981.118,958.449,961.107,521143220,20442229000.000
        成交量：股 820953530  821万手
        成交额：元 16959251000.000 169.6亿
        """
        # 0.参数校验
        if not index_code.startswith('8'):
            raise RuntimeError('index_code错误，是8开头的指数代码,')
        # 1.接口 url
        api_url = f"http://d.10jqka.com.cn/v6/line/48_{index_code}/{k_type - 1}{adjust_type}/last1800.js"
        # 同花顺可能ip限制，降低请求次数
        text = self._get_text(api_url, index_code)
        if THS_IP_LIMIT_RES in text:
            return Exception(THS_IP_LIMIT_MSG)
        result_text = text[text.index('{'):-1]
        data_list = json.loads(result_text)['data'].split(';')
        data = []
        for d in data_list:
            data.append(str(d).split(',')[0:7])
        result_df = pd.DataFrame(data=data, columns=['trade_date', 'open', 'high', 'low', 'close', 'volume', 'amount'])
        result_df['index_code'] = index_code
        result_df['trade_time'] = pd.to_datetime(result_df['trade_date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        result_df['trade_date'] = pd.to_datetime(result_df['trade_date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
        result_df['close'] = result_df['close'].astype(float)
        result_df['change'] = result_df['close'] - result_df['close'].shift(1)
        result_df['change_pct'] = result_df['change'] / result_df['close'].shift(1) * 100

        # 3. 清洗数据
        result_df = result_df.round(2)
        result_df['close'] = result_df['close'].apply(lambda x: format(x, '.2f'))
        result_df.replace('--', None, inplace=True)
        result_df.replace('', None, inplace=True)
        result_df.replace(np.nan, None, inplace=True)
        return result_df[self.__MARKET_COLUMNS]

    def get_market_concept_min_ths(self, index_code='886041'):
        """
        获取概念行情当日分时
        web： http://d.10jqka.com.cn/v6/time/48_886013/last.js
        0930,958.901,74456973,36.807,2022925;  "pre": "960.374",
        :param index_code: 概念指数代码
        :return 时间，现价，成交额（元），均价，成交量（股） 涨跌额，涨跌幅
        'index_code', 'trade_time', 'price', 'change', 'change_pct', 'volume', 'avg_price', 'amount'
        """
        # 0.参数校验
        if not index_code.startswith('8'):
            raise RuntimeError('index_code错误，是8开头的指数代码,')
        # 1.接口 url
        api_url = f"http://d.10jqka.com.cn/v6/time/48_{index_code}/last.js"
        text = self._get_text(api_url, index_code)
        if THS_IP_LIMIT_RES in text:
            return Exception(THS_IP_LIMIT_MSG)
        # 2. 解析数据
        result_json = json.loads(text[text.index('{'):-1])[f"48_{index_code}"]
        pre_price = result_json['pre']
        trade_date = result_json['date']
        data_list = result_json['data'].split(';')
        data = []
        for d in data_list:
            data.append(str(d).split(','))
        # 3. 封装数据
        result_df = pd.DataFrame(data=data, columns=['trade_time', 'price', 'amount', 'avg_price', 'volume'])
        result_df['index_code'] = index_code
        result_df['trade_time'] = trade_date + result_df['trade_time']
        result_df['trade_date'] = pd.to_datetime(trade_date, format='%Y%m%d').strftime('%Y-%m-%d')
        result_df['trade_time'] = pd.to_datetime(result_df['trade_time'], format='%Y%m%d%H%M').dt.strftime(
            '%Y-%m-%d %H:%M:%S')
        result_df['price'] = result_df['price']
        result_df['change'] = result_df['price'].astype(float) - float(pre_price)
        result_df['change_pct'] = result_df['change'] / float(pre_price) * 100
        result_df.replace('--', None, inplace=True)
        result_df.replace('', None, inplace=True)
        result_df.replace(np.nan, None, inplace=True)
        return result_df[self.__MARKET_CONCEPT_MIN_COLUMNS]

    def get_market_concept_current_ths(self, index_code: str = '886013', k_type: int = 1):
        """
        获取同花顺当前的概念行情
        web: http://q.10jqka.com.cn/gn/
        pc: http://d.10jqka.com.cn/v6/line/48_886042/01/today.js
        quotebridge_v6_line_48_886042_01_today({"48_886042":{"1":"20230425","7":"891.344","8":"892.350","9":"853.800",
        "11":"860.076","13":491708080,"19":"17647511000.000","74":"","1968584":"","66":"","open":1,"dt":"2244",
        "name":"\u5b58\u50a8\u82af\u7247","marketType":""}})

        :param index_code: 同花顺概念指数代码
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :return: k线行情数据 [概念代码,交易时间，交易日期，开，高，低，当前价格,成交量，成交额]
        ;20230419,958.901,981.118,958.449,961.107,521143220,20442229000.000,存储芯片
        k:   1,      7,      8,       9,      11,      13,         19,        name
        成交量：股 820953530  821万手
        成交额：元 16959251000.000 169.6亿
        """
        # 0.参数校验
        if not index_code.startswith('8'):
            raise RuntimeError('index_code错误，是8开头的指数代码,')
        # 1.接口 url
        api_url = f"http://d.10jqka.com.cn/v6/line/48_{index_code}/{k_type - 1}1/today.js"
        headers = copy.deepcopy(ths_headers.text_headers)
        headers['Host'] = 'd.10jqka.com.cn'
        # 同花顺可能ip限制，降低请求次数
        text = self._get_text(api_url, index_code)
        if THS_IP_LIMIT_RES in text:
            return Exception(THS_IP_LIMIT_MSG)
        result_text = text[text.index('{'):-1]
        data_list = [json.loads(result_text)[f"48_{index_code}"]]
        rename = {'1': 'trade_date', '7': 'open', '8': 'high', '9': 'low', '11': 'price', '13': 'volume',
                  '19': 'amount', 'open': 'status'}
        result_df = pd.DataFrame(data=data_list).rename(columns=rename)
        result_df['trade_time'] = result_df['trade_date'] + result_df['dt']
        result_df['trade_time'] = pd.to_datetime(result_df['trade_time'], format='%Y%m%d%H%M').dt.strftime(
            '%Y-%m-%d %H:%M:%S')
        columns = ['trade_time', 'trade_date', 'open', 'high', 'low', 'price', 'volume', 'amount']
        result_df = result_df[columns]
        result_df['index_code'] = index_code
        result_df['trade_date'] = pd.to_datetime(result_df['trade_date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
        return result_df[self.__MARKET_CONCEPT_CURRENT_COLUMNS]


if __name__ == '__main__':
    print(ConceptMarketThs().get_market_concept_ths(index_code='886041'))
    print(ConceptMarketThs().get_market_concept_min_ths(index_code='886041'))
    print(ConceptMarketThs().get_market_concept_current_ths(index_code='886041'))
