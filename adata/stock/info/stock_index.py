# -*- coding: utf-8 -*-
"""
@desc:
a股指数
上交所
http://www.sse.com.cn/market/sseindex/indexlist/
深交所
http://www.szse.cn/market/exponent/sample/index.html

同花顺
http://q.10jqka.com.cn/zs/

东方财富
http://quote.eastmoney.com/center/gridlist.html#index_sh
http://quote.eastmoney.com/center/gridlist.html#index_sz

指数成分：只用同花顺和东方财富，新浪和百度目前都不准确
@author: 1nchaos
@time: 2023/5/23
@log: change log
"""
import copy

import pandas as pd
from bs4 import BeautifulSoup

from adata.common.exception.exception_msg import *
from adata.common.headers import ths_headers
from adata.common.utils import cookie, requests
from adata.stock.cache.index_code_rel_ths import rel


class StockIndex(object):
    """
    A股指数
    """
    __INDEX_CONSTITUENT_COLUMN = ['index_code', 'stock_code', 'short_name']
    __INDEX_CODE_COLUMN = ['index_code', 'concept_code', 'name', 'source']

    def __init__(self) -> None:
        super().__init__()

    def all_index_code(self):
        """
        获取所有A股市场的指数的代码
        目前主要来源：同花顺,
        concept_code为同花顺的概念代码
        :return: 指数信息[name,index_code,concept_code,source]
        """
        return self.__all_index_code_ths()

    def __all_index_code_ths(self):
        """
        获取同花顺所有行情中心的指数代码
        http://q.10jqka.com.cn/zs/
        上面地址可不用翻页
        :return: 指数信息[name,index_code，concept_code,source]
        """
        # 1. url拼接页码等参数
        data = []
        total_pages = 1
        curr_page = 1
        while curr_page <= total_pages:
            api_url = f"http://q.10jqka.com.cn/zs/index/field/zdf/order/desc/page/{curr_page}/ajax/1/"
            headers = copy.deepcopy(ths_headers.text_headers)
            headers['Cookie'] = cookie.ths_cookie()
            res = requests.request(method='get', url=api_url, headers=headers, proxies={})
            curr_page += 1
            # 2. 判断请求是否成功
            if res.status_code != 200:
                continue
            text = res.text
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
                    a_href = tds[1].find('a')
                    page_data.append({'index_code': tds[1].contents[0].text,
                                      'concept_code': a_href['href'].split('/')[-2],
                                      'name': tds[2].contents[0].text, 'source': '同花顺'})
            data.extend(page_data)
        # 5. 封装数据
        if not data:
            return pd.DataFrame(data=data, columns=self.__INDEX_CODE_COLUMN)
        result_df = pd.DataFrame(data=data)
        data.clear()
        return result_df[self.__INDEX_CODE_COLUMN]

    def index_constituent(self, index_code=None, wait_time=None):
        """
        获取对应指数的成分股
        ps:百度和新浪的数据有问题，丢弃这两个数据源，优先使用同花顺
        :param index_code: 指数代码
        :param wait_time: 等待时间：毫秒；表示每个请求的间隔时间，主要用于防止请求太频繁的限制。
        :return: ['index_code', 'stock_code', 'short_name']
        """
        # res = self.__index_constituent_sina(index_code=index_code)
        # if not res.empty:
        #     return res
        return self.__index_constituent_ths(index_code=index_code, wait_time=wait_time)

    def __index_constituent_ths(self, index_code=None, wait_time=None):
        """
        同花顺指数成分股
        :param index_code: 指数代码 399282
        :param wait_time: 等待时间：毫秒；表示每个请求的间隔时间，主要用于防止请求太频繁的限制。
        :return:['index_code', 'stock_code', 'short_name']
        """
        # 转换抓取的code,
        catch_code = rel[index_code] if index_code.startswith('0') and index_code in rel.keys() else index_code
        # 转换指数代码
        index_code = rel[index_code] if ('A' in index_code or 'B' in index_code or 'C' in index_code) and index_code in rel.keys() else index_code
        # 1. url拼接页码等参数
        data = []
        total_pages = 1
        curr_page = 1
        while curr_page <= total_pages:
            api_url = f"http://q.10jqka.com.cn/zs/detail/field/199112/order/desc/page/" \
                      f"{curr_page}/ajax/1/code/{catch_code}"
            headers = copy.deepcopy(ths_headers.text_headers)
            headers['Cookie'] = cookie.ths_cookie()
            res = requests.request(method='get', url=api_url, headers=headers, proxies={}, wait_time=wait_time)
            curr_page += 1
            # 2. 判断请求是否成功
            if res.status_code != 200:
                continue
            text = res.text
            if THS_IP_LIMIT_RES in res:
                raise Exception(THS_IP_LIMIT_MSG)
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
                    page_data.append({'index_code': index_code, 'stock_code': tds[1].contents[0].text,
                                      'short_name': tds[2].contents[0].text})
            data.extend(page_data)
        # 5. 封装数据
        if not data:
            return pd.DataFrame(data=data, columns=self.__INDEX_CONSTITUENT_COLUMN)
        result_df = pd.DataFrame(data=data)
        data.clear()
        return result_df[self.__INDEX_CONSTITUENT_COLUMN]

    def __index_constituent_baidu(self, index_code=None):
        """
        https://gushitong.baidu.com/opendata?resource_id=5352&query=000133&code=000133&market=ab&group=asyn_ranking&pn=100&rn=50&pc_web=1&finClientType=pc
        百度指数成分股，目前接口存在bug
        :param index_code: 指数代码 399282
        :return:['index_code', 'stock_code', 'short_name']
        """
        # 1.请求接口 url
        data = []
        for page in range(100):
            api_url = f"https://gushitong.baidu.com/opendata?resource_id=5352&query={index_code}&code={index_code}&" \
                      f"market=ab&group=asyn_ranking&pn={page * 50}&rn=100&pc_web=1&finClientType=pc"
            res = requests.request('get', api_url, headers={})

            # 2. 判断结果是否正确
            if len(res.text) < 1 or res.status_code != 200:
                break
            res_json = res.json()
            if res_json['ResultCode'] != '0':
                break
            # 3.解析数据
            # 3.1 空数据时返回为空
            result = res_json['Result']
            if not result:
                break

            # 3.2 正常解析数据
            try:
                result_list = result[-1]['DisplayData']['resultData']['tplData']['result']['list']
                data.extend(result_list)
            except KeyError:
                break

        # 4. 封装数据
        result_df = pd.DataFrame(data=data).rename(columns={'code': 'stock_code', 'name': 'short_name'})
        result_df['index_code'] = index_code
        data.clear()
        return result_df[self.__INDEX_CONSTITUENT_COLUMN]

    def __index_constituent_sina(self, index_code=None, wait_time=None):
        """
        http://vip.stock.finance.sina.com.cn/corp/view/vII_NewestComponent.php?page=1&indexid=000099
        新浪指数成分：目前数据不准确
        :param index_code: 指数代码 399282
        :return:['index_code', 'stock_code', 'short_name']
        """
        # 1. url拼接页码等参数
        data = []
        total_pages = 1
        curr_page = 1
        while curr_page <= total_pages:
            api_url = f"http://vip.stock.finance.sina.com.cn/corp/view/vII_NewestComponent.php?" \
                      f"page={curr_page}&indexid={index_code}"

            res = requests.request(method='get', url=api_url, proxies={}, wait_time=wait_time)
            curr_page += 1
            # 2. 判断请求是否成功
            if res.status_code != 200:
                continue
            text = res.text
            if 'NewStockTable' not in text or '最新成分' not in text:
                break
            soup = BeautifulSoup(text, 'html.parser')
            # 3 .获取总的页数
            if total_pages == 1:
                page_info = soup.find('table', {'class': 'table2'}).text
                if page_info and '共' in page_info and '页' in page_info:
                    # Extract the total number of pages from the page_info string
                    total_pages = int(page_info.split('共')[1].split('页')[0])
            # 4. 解析数据
            page_data = []
            table = soup.find('table', {'id': 'NewStockTable'})
            for row in table.find_all('tr')[2:]:
                cells = row.find_all('td')
                if len(cells) == 3:
                    page_data.append({'index_code': index_code, 'stock_code': cells[0].div.text.strip(),
                                      'short_name': cells[1].div.text.strip()})
            data.extend(page_data)
        # 5. 封装数据
        if not data:
            return pd.DataFrame(data=data, columns=self.__INDEX_CONSTITUENT_COLUMN)
        result_df = pd.DataFrame(data=data)
        data.clear()
        return result_df[self.__INDEX_CONSTITUENT_COLUMN]


if __name__ == '__main__':
    print(StockIndex().all_index_code())
    print(StockIndex().index_constituent(index_code='000033'))
    print(StockIndex().index_constituent(index_code='399387', wait_time=158))
