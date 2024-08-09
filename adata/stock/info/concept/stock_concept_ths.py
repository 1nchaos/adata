# -*- coding: utf-8 -*-
"""
@summary: 股票概念
同花顺概念更及时和完整，同花顺的股票概念抓取

概念，指数成分
来源于同花顺
http://q.10jqka.com.cn/gn

https://basic.10jqka.com.cn/000002/concept.html?cid=308717#ifind

https://d.10jqka.com.cn/v4/stockblock/hs_600769/last.js
https://m.10jqka.com.cn/stockpage/hs_600769/#&atab=pankou

@author: 1nchaos
@date: 2023/3/30 16:17
"""
import copy
import json
import math

import pandas as pd
from bs4 import BeautifulSoup

from adata.common.exception.exception_msg import *
from adata.common.headers import ths_headers
from adata.common.utils import cookie
from adata.common.utils import requests
from adata.stock.info.concept.stock_concept_template import StockConceptTemplate


class StockConceptThs(StockConceptTemplate):

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
        result_df = pd.concat([result_df_l, result_df_r]).drop_duplicates(keep='first', inplace=False,
                                                                          ignore_index=True)

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

    def concept_constituent_ths(self, concept_code=None, name=None, index_code=None, wait_time=None):
        """
        获取同花顺概念成分
        优先级
        index_code >  name > concept_code: 三选其一
        指数代码来自app，名称查询来自问财，概念代码来自网页；
        :param wait_time: 等待时间：毫秒；表示每个请求的间隔时间，主要用于防止请求太频繁的限制。
        :param concept_code: 概念代码，3开头
        :param index_code: 指数代码，8开头
        :param name: 概念名称
        :return: 概念的成分股
        """
        if concept_code:
            return self.__index_constituent_ths_by_concept_code(concept_code=concept_code, wait_time=wait_time)
        elif name:
            return self.__index_constituent_ths_by_name(name=name, wait_time=wait_time)
        elif index_code:
            return self.__index_constituent_ths_by_index_code(index_code=index_code, wait_time=wait_time)
        else:
            return pd.DataFrame(data=[], columns=self._CONCEPT_CONSTITUENT_COLUMNS)

    def __index_constituent_ths_by_concept_code(self, concept_code=None, wait_time=None):
        """
        同花顺概念成分股
        web_url :http://q.10jqka.com.cn/gn/detail/field/199112/order/desc/page/1/ajax/1/code/301539
        answer: http://www.iwencai.com/gateway/urp/v7/landing/getDataList?query=chatgpt%20%E6%A6%82%E5%BF%B5%E6%88%90%E5%88%86&page=1&perpage=100&query_type=stock&comp_id=6734520&uuid=24087
        :param concept_code: 概念代码： 301539
        :param wait_time: 等待时间：表示每个请求的间隔时间，主要用于防止请求太频繁的限制。
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
            res = requests.request(method='get', url=api_url, headers=headers, proxies={}, wait_time=wait_time)
            curr_page += 1
            # 2. 判断请求是否成功
            if res.status_code != 200:
                continue
            text = res.text
            if THS_IP_LIMIT_RES in text:
                return Exception(THS_IP_LIMIT_MSG)
            if '暂无成份股数据' in text or '概念板块' in text or '概念时间表' in text:
                break
            soup = BeautifulSoup(text, 'html.parser')
            # 3 .获取总的页数
            if total_pages == 1:
                page_info = soup.find('span', {'class': 'page_info'})
                if page_info:
                    total_pages = int(page_info.text.split("/")[1])
                    # 只能获取到前5页
                    if total_pages > 5:
                        total_pages = 5
            # 4. 解析数据
            page_data = []
            for idx, tr in enumerate(soup.find_all('tr')):
                if idx != 0:
                    tds = tr.find_all('td')
                    page_data.append({'stock_code': tds[1].contents[0].text, 'short_name': tds[2].contents[0].text})
            data.extend(page_data)
        # 5. 封装数据
        if not data:
            return pd.DataFrame(data=data, columns=self._CONCEPT_CONSTITUENT_COLUMNS)
        result_df = pd.DataFrame(data=data)
        data.clear()
        return result_df[self._CONCEPT_CONSTITUENT_COLUMNS]

    def __index_constituent_ths_by_index_code(self, index_code=None, wait_time=None):
        """
        根据概念指数代码获取成分股
        web_url： https://d.10jqka.com.cn/v2/blockrank/885338/8/d3000.js
        :param index_code: 指数代码，ths 8开头
        :param wait_time: 等待时间：表示每个请求的间隔时间，主要用于防止请求太频繁的限制。
        :return: ['stock_code', 'short_name']
        """
        # 1.接口 url
        api_url = f"https://d.10jqka.com.cn/v2/blockrank/{index_code}/8/d15.js"
        headers = copy.deepcopy(ths_headers.text_headers)
        headers['Host'] = 'd.10jqka.com.cn'
        res = requests.request(method='get', url=api_url, headers=headers, proxies={}, wait_time=wait_time)
        # 同花顺可能ip限制，降低请求次数
        text = res.text
        if THS_IP_LIMIT_RES in text:
            return Exception(THS_IP_LIMIT_MSG)
        # 2. 解析总数
        result_json = json.loads(text[text.index('{'):-1])
        total_count = float(result_json['block']['subcodeCount'])
        if total_count < 2500:
            total_num = math.ceil(total_count / 15) * 15
            apis = [f"https://d.10jqka.com.cn/v2/blockrank/{index_code}/8/d{total_num}.js"]
        else:
            apis = [f"https://d.10jqka.com.cn/v2/blockrank/{index_code}/8/a2500.js",
                    f"https://d.10jqka.com.cn/v2/blockrank/{index_code}/8/d2500.js"]
        data_list = []

        # 3. 请求所有数据
        for api_url in apis:
            res = requests.request(method='get', url=api_url, headers=headers, proxies={}, wait_time=wait_time)
            text = res.text
            result_json = json.loads(text[text.index('{'):-1])
            items = result_json['items']
            data_list.extend(items)

        # 4. 数据封装，去重
        rename = {'5': 'stock_code', '55': 'short_name'}
        result_df = pd.DataFrame(data=data_list).rename(columns=rename)
        result_df = result_df.drop_duplicates(subset=['stock_code'], keep='last', ignore_index=True)
        return result_df[self._CONCEPT_CONSTITUENT_COLUMNS]

    def __index_constituent_ths_by_name(self, name=None, wait_time=None):
        """
        同花顺概念成分股，通过问财询问
        answer: http://www.iwencai.com/gateway/urp/v7/landing/getDataList?query=chatgpt%20%E6%A6%82%E5%BF%B5%E6%88%90%E5%88%86&page=1&perpage=100&query_type=stock&comp_id=6734520&uuid=24087
        :param name: 概念名称
        :param wait_time: 等待时间：表示每个请求的间隔时间，主要用于防止请求太频繁的限制。
        :return:['concept_code', 'stock_code', 'short_name']
        """
        # 1. url拼接页码等参数
        data = []
        total_pages = 1
        curr_page = 1
        while curr_page <= total_pages:
            api_url = f"http://www.iwencai.com/gateway/urp/v7/landing/getDataList?query={name} 概念成分股有哪些&" \
                      f"urp_sort_way=desc&urp_sort_index=最新涨跌幅&page={curr_page}&perpage=100&addheaderindexes=&codelist=&" \
                      f"indexnamelimit=&ret=json_all&date_range[0]=20240809&urp_use_sort=1&query_type=stock&" \
                      f"comp_id=6836372&business_cat=soniu&uuid=24087"
            headers = copy.deepcopy(ths_headers.json_headers)
            headers['Host'] = 'www.iwencai.com'
            headers['Sec-Fetch-Mode'] = 'navigate'
            res = requests.request(method='post', url=api_url, headers=headers, proxies={}, wait_time=wait_time)
            curr_page += 1
            # 2. 判断请求是否成功
            if res.status_code != 200:
                continue
            text = res.text.encode('utf-8').decode('unicode escape')
            if THS_IP_LIMIT_RES in text:
                return Exception(THS_IP_LIMIT_MSG)
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
            return pd.DataFrame(data=data, columns=self._CONCEPT_CONSTITUENT_COLUMNS)
        result_df = pd.DataFrame(data=data)
        data.clear()
        return result_df[self._CONCEPT_CONSTITUENT_COLUMNS]

    def get_concept_ths(self, stock_code: str = '000001'):
        """
        根据股票代码获取，股票所属的所有的概念信息
        https://basic.10jqka.com.cn/300033/concept.html
        :param stock_code: 股票代码
        :return: 概念信息
        """
        url = f"https://basic.10jqka.com.cn/{stock_code}/concept.html"
        headers = ths_headers.text_headers
        headers['Host'] = 'basic.10jqka.com.cn'
        res = requests.request('get', url, headers=headers, proxies={})
        # 3. 解析数据
        text = res.content.decode('gbk')
        soup = BeautifulSoup(text, 'html.parser')
        table = soup.find('table', attrs={'class': 'gnContent'})
        trs = table.tbody.find_all('tr')
        data = []
        for i in range(0, len(trs), 2):
            columns = trs[i].find_all('td')
            data.append({'stock_code': stock_code, 'concept_code': columns[1].get('clid'),
                         'name': columns[1].text,
                         'reason': trs[i + 1].text, 'source': '同花顺'})
        result_df = pd.DataFrame(data=data, columns=self._CONCEPT_INFO_COLUMNS)
        result_df.replace(to_replace=[r'\t', r'\n', ' '], value='', regex=True, inplace=True)
        return result_df


if __name__ == '__main__':
    print(StockConceptThs().all_concept_code_ths())
    print(StockConceptThs().concept_constituent_ths(name='生物医药'))
    print(StockConceptThs().concept_constituent_ths(index_code='885403'))
    print(StockConceptThs().concept_constituent_ths(concept_code='300769'))
