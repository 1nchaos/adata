# -*- coding: utf-8 -*-
"""
@summary: 股票概念
同花顺概念更及时和完整，所以目前暂只基于同花顺的股票概念抓取

概念，指数成分
来源于同花顺
http://q.10jqka.com.cn/gn
@author: 1nchaos
@date: 2023/3/30 16:17
"""
import copy
import math

import pandas as pd
from bs4 import BeautifulSoup

from adata.common.headers import ths_headers
from adata.common.utils import cookie
from adata.common.utils import requests


class StockConcept(object):
    """
    股票概念
    """
    CONCEPT_CONSTITUENT_COLUMNS = ['stock_code', 'short_name']
    CONCEPT_CODE_COLUMNS = ['concept_code', 'index_code', 'name', 'source']

    def __init__(self) -> None:
        super().__init__()

    def all_concept_code_ths(self):
        """
        获取同花顺概念列表：名称,指数代码，概念代码
        特别注意：
        同花顺概念指数代码是8开头
        概念代码是3开头
        这两个不要混淆啦，同花顺的网站获取数据需要用到这两个代码
        :return: 概念[[name,index_code，concept_code]]
        """
        index_df = self.__concept_index_code_ths()
        code_df = self.__concept_code_ths()
        result_df_l = pd.merge(index_df, code_df, how='left', on='name')
        result_df_r = pd.merge(index_df, code_df, how='right', on='name')
        result_df = result_df_l.append(result_df_r).drop_duplicates(keep='first', inplace=False, ignore_index=True)

        index_df.drop(index_df.index, inplace=True)
        code_df.drop(code_df.index, inplace=True)
        result_df_l.drop(result_df_l.index, inplace=True)
        result_df_r.drop(result_df_r.index, inplace=True)
        result_df['source'] = '同花顺'
        return result_df

    def __concept_code_ths(self):
        """
        获取同花顺的所有概念和概念代码,暂时废弃
        web: http://q.10jqka.com.cn/gn/
        """
        # 1. 请求接口 url
        api_url = f"http://q.10jqka.com.cn/gn/"
        for i in range(3):
            res = requests.request('get', api_url, headers=ths_headers.text_headers, proxies={})
            # 2. 判断请求是否正确
            text = res.text
            if res.status_code != 200 or len(text) < 1:
                continue
            # 3. 解析数据
            soup = BeautifulSoup(text, 'html.parser')
            data = []
            for a in soup.find_all('a'):
                href = str(a['href'])
                if href.startswith(api_url + 'detail/code/'):
                    data.append([href[-7: -1], a.string, href])

            # 4. 封装数据
            data_df = pd.DataFrame(data=data, columns=['concept_code', 'name', 'href'])[['concept_code', 'name']]
            return data_df

    def __concept_index_code_ths(self):
        """
        获取app的概率列表，通过问财询问得到结果
        :return: app的概念列表： concept_code，name
        """
        data = []
        for i in range(1, 10):
            api_url = f"http://search.10jqka.com.cn/gateway/urp/v7/landing/getDataList?perpage=100&page={i}&query=%E6%89%80%E6%9C%89%E6%A6%82%E5%BF%B5&condition=%5B%7B%22indexName%22%3A%22%E6%8C%87%E6%95%B0%40%E5%90%8C%E8%8A%B1%E9%A1%BA%E6%A6%82%E5%BF%B5%E6%8C%87%E6%95%B0%22%2C%22indexProperties%22%3A%5B%5D%2C%22source%22%3A%22new_parser%22%2C%22type%22%3A%22index%22%2C%22indexPropertiesMap%22%3A%7B%7D%2C%22reportType%22%3A%22null%22%2C%22chunkedResult%22%3A%22%E6%89%80%E6%9C%89%E6%A6%82%E5%BF%B5%22%2C%22valueType%22%3A%22_%E6%8C%87%E6%95%B0%E7%B1%BB%E5%9E%8B%22%2C%22domain%22%3A%22abs_a%E6%8C%87%E9%A2%86%E5%9F%9F%22%2C%22uiText%22%3A%22%E5%90%8C%E8%8A%B1%E9%A1%BA%E6%A6%82%E5%BF%B5%E6%8C%87%E6%95%B0%22%2C%22sonSize%22%3A0%2C%22queryText%22%3A%22%E5%90%8C%E8%8A%B1%E9%A1%BA%E6%A6%82%E5%BF%B5%E6%8C%87%E6%95%B0%22%2C%22relatedSize%22%3A0%7D%5D&urp_sort_index=%E6%8C%87%E6%95%B0%E4%BB%A3%E7%A0%81&source=Ths_iwencai_Xuangu&urp_sort_way=desc&codelist=&page_id=&logid=35df00ee5ae706d0dfcd0dbfdb846e0c&ret=json_all&sessionid=35df00ee5ae706d0dfcd0dbfdb846e0c&iwc_token=0ac9667016801698001765831&user_id=Ths_iwencai_Xuangu_7fahywzhbkrh4lwwkwfw936njqbjzsly&uuids%5B0%5D=23119&query_type=zhishu&comp_id=6367801&business_cat=soniu&uuid=23119"
            res = requests.request('get', url=api_url, headers=ths_headers.c_headers)
            res_json = res.json()
            if res_json['status_msg'] == 'ok':
                data_list = res_json['answer']['components'][0]['data']['datas']
                if len(data_list) < 1:
                    break
                for d in data_list:
                    data.append([d['code'], d['指数简称']])
        data_df = pd.DataFrame(data=data, columns=['index_code', 'name']).drop_duplicates(keep='first', inplace=False,
                                                                                          ignore_index=True)
        return data_df

    def concept_constituent_ths(self, concept_code=None, name=None):
        """
        获取同花顺概念成分，推荐使用概念名称进行查询，名称查询来自问财，概念代码来自网页
        :param concept_code: 概念代码，3开头
        :param name: 概念名称
        :return: 概念的成分股
        """
        if concept_code:
            return self.__concept_constituent_ths_by_code(concept_code=concept_code)
        elif name:
            return self.__index_constituent_ths_by_name(name=name)
        else:
            return pd.DataFrame(data=[], columns=self.CONCEPT_CONSTITUENT_COLUMNS)

    def __concept_constituent_ths_by_code(self, concept_code=None):
        """
        同花顺概念成分股
        web_url :http://q.10jqka.com.cn/gn/detail/field/199112/order/desc/page/1/ajax/1/code/301539
        answer: http://www.iwencai.com/gateway/urp/v7/landing/getDataList?query=chatgpt%20%E6%A6%82%E5%BF%B5%E6%88%90%E5%88%86&page=1&perpage=100&query_type=stock&comp_id=6734520&uuid=24087
        :param concept_code: 概念代码： 301539
        :return:['concept_code', 'stock_code', 'short_name']
        """
        # 1. url拼接页码等参数
        data = []
        total_pages = 1
        curr_page = 1
        while curr_page <= total_pages:
            api_url = f"http://q.10jqka.com.cn/gn/detail/field/199112/order/desc/page/" \
                      f"{curr_page}/ajax/1/code/{concept_code}"
            headers = copy.deepcopy(ths_headers.text_headers)
            headers['Cookie'] = cookie.ths_cookie()
            res = requests.request(method='get', url=api_url, headers=headers, proxies={})
            curr_page += 1
            # 2. 判断请求是否成功
            if res.status_code != 200:
                continue
            text = res.text
            if '暂无成份股数据' in text or '概念板块' in text or '概念时间表' in text:
                break
            soup = BeautifulSoup(text, 'html.parser')
            # 3 .获取总的页数
            if total_pages == 1:
                page_info = soup.find('span', {'class': 'page_info'})
                if page_info:
                    total_pages = int(page_info.text.split("/")[1])
            # 4. 解析数据
            page_data = []
            for idx, tr in enumerate(soup.find_all('tr')):
                if idx != 0:
                    tds = tr.find_all('td')
                    page_data.append({'stock_code': tds[1].contents[0].text, 'short_name': tds[2].contents[0].text})
            data.extend(page_data)
        # 5. 封装数据
        if not data:
            return pd.DataFrame(data=data, columns=self.CONCEPT_CONSTITUENT_COLUMNS)
        result_df = pd.DataFrame(data=data)
        data.clear()
        return result_df[self.CONCEPT_CONSTITUENT_COLUMNS]

    def __index_constituent_ths_by_name(self, name=None):
        """
        同花顺概念成分股，通过问财询问
        answer: http://www.iwencai.com/gateway/urp/v7/landing/getDataList?query=chatgpt%20%E6%A6%82%E5%BF%B5%E6%88%90%E5%88%86&page=1&perpage=100&query_type=stock&comp_id=6734520&uuid=24087
        :param name: 概念名称
        :return:['concept_code', 'stock_code', 'short_name']
        """
        # 1. url拼接页码等参数
        data = []
        total_pages = 1
        curr_page = 1
        while curr_page <= total_pages:
            api_url = f"https://www.iwencai.com/gateway/urp/v7/landing/getDataList?query={name} 概念成分&" \
                      f"page={curr_page}&perpage=100&query_type=stock&comp_id=6734520&uuid=24087"
            headers = copy.deepcopy(ths_headers.json_headers)
            headers['Host'] = 'www.iwencai.com'
            headers['Sec-Fetch-Mode'] = 'navigate'
            res = requests.request(method='get', url=api_url, headers=headers, proxies={})
            curr_page += 1
            # 2. 判断请求是否成功
            if res.status_code != 200:
                continue
            text = res.text.encode('utf-8').decode('unicode escape')
            if name not in text:
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
                if (name == one['所属概念']) or \
                        ('所属指数类' in one.keys() and (name == one['所属指数类'] or f"{name};" in one['所属指数类'])):
                    page_data.append({'stock_code': one['code'], 'short_name': one['股票简称'], '': ''})
            data.extend(page_data)
        # 5. 封装数据
        if not data:
            return pd.DataFrame(data=data, columns=self.CONCEPT_CONSTITUENT_COLUMNS)
        result_df = pd.DataFrame(data=data)
        data.clear()
        return result_df[self.CONCEPT_CONSTITUENT_COLUMNS]


if __name__ == '__main__':
    print(StockConcept().all_concept_code_ths())
    print(StockConcept().concept_constituent_ths(name='东数西算（算力）'))
