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

import pandas as pd
from bs4 import BeautifulSoup

from adata.common.utils import requests


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
        return self.__all_index_code_east()

    def __all_index_code_east(self, wait_time=0):
        """
        东方财富指数列表
        https://quote.eastmoney.com/center/gridlist.html#index_sh
        https://39.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&dect=1&wbp2u=|0|0|0|web&fid=f3&fs=m:1+s:2&fields=f12,f14&_=1720430951494
        :return: 指数信息[name,index_code，concept_code,source]
        """
        data = []
        for i in range(2):
            curr_page = 1
            while curr_page < 88:
                if i == 0:
                    url = f"https://39.push2.eastmoney.com/api/qt/clist/get?" \
                          f"pn={curr_page}&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&" \
                          f"dect=1&wbp2u=|0|0|0|web&fid=f3&fs=m:1+s:2&fields=f12,f13,f14&_=1720430951494"
                else:
                    url = f"https://31.push2.eastmoney.com/api/qt/clist/get?" \
                          f"pn={curr_page}&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&dect=1&" \
                          f"wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:5&fields=f12,f13,f14&_=1720432207117"
                res_json = requests.request('get', url, headers={}, proxies={}, wait_time=wait_time).json()
                res_data = res_json['data']
                if not res_data:
                    break
                res_data = res_data['diff']
                for _ in res_data:
                    data.append({'cid': _['f13'], 'index_code': _['f12'], 'name': _['f14'], 'source': '东方财富',
                                 'concept_code': ''})
                curr_page += 1
        result_df = pd.DataFrame(data=data)
        return result_df[self.__INDEX_CODE_COLUMN]

    def index_constituent(self, index_code=None, wait_time=None):
        """
        获取对应指数的成分股
        ps:百度和新浪的数据有问题，丢弃这两个数据源，优先使用同花顺
        :param index_code: 指数代码
        :param wait_time: 等待时间：毫秒；表示每个请求的间隔时间，主要用于防止请求太频繁的限制。
        :return: ['index_code', 'stock_code', 'short_name']
        """
        return self.__index_constituent_baidu(index_code=index_code)

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
        result_df = result_df[self.__INDEX_CONSTITUENT_COLUMN]
        result_df = result_df.drop_duplicates()
        return result_df

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
    print(StockIndex().index_constituent(index_code='000113'))
