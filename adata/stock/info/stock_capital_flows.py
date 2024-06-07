# -*- coding: utf-8 -*-
"""
@desc: 股票资金流向

东方财富：个股
https://data.eastmoney.com/zjlx/600519.html

@author: 1nchaos
@time: 2024/6/7
@log: change log
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


class StockCapitalFlows(object):
    
    
    def __init__(self) -> None:
        super().__init__()
    
    @classmethod
    def get_html_source_code(cls, url):
        # 初始化playwright
        with sync_playwright() as p:
            # 启动浏览器并创建一个页面
            browser = p.chromium.launch()
            page = browser.new_page()

            # 打开目标网页
            page.goto(url)

            # 等待页面加载完成，可以根据实际情况调整等待条件
            page.wait_for_load_state()

            # 读取并打印网页源代码
            source_code = page.content()
            #print(source_code)        

            # 关闭浏览器
            browser.close()
            
        return source_code

        
    def get_inflow(self,stock_code):
        __INFLOW_COLUMNS = ['stock_code', 
                      'trade_date', 
                      'close', 
                      'change_pct',
                      'major_inflow',
                      'major_inflow_pct',
                      'very_large_inflow',
                      'very_large_inflow_pct',
                      'large_inflow',
                      'large_inflow_pct',
                      'medium_inflow',
                      'medium_inflow_pct',
                      'small_inflow',
                      'small_inflow_pct']
        
        # 股票代码，例如 '000001' 对应平安银行
        # stock_code = '000001'

        # 东方财富网资金流向数据的URL，需要根据实际情况调整
        url = f'https://data.eastmoney.com/zjlx/{stock_code}.html'

        # 发送HTTP请求
        response = requests.get(url)
        # fhandle=open('temp.html','wb'); fhandle.write(response); fhandle.close
        response.encoding = 'utf-8'  # 确保编码正确

        # 检查请求是否成功
        if response.status_code == 200:
            
            source_code=self.get_html_source_code(url)
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(source_code, 'html.parser')
            
            
            # 根据东方财富网的页面结构找到资金流向数据所在的表格
            # 注意：这里的选择器需要根据实际页面结构进行调整
            table = soup.find('div', attrs={'id': 'table_ls'})
            
            # 读取表格数据
            data = []
            headers= __INFLOW_COLUMNS
            
            '''
            print(table)
            # 首先读取表头
            headers_row = table.find('tr')
            print(headers_row)
            headers = [th.text.strip() for th in headers_row.find_all('th')]
            print(headers)
            '''           
            
            # 然后读取表格内容
            #print(table.find_all('tr'))
            for row in table.find_all('tr')[2:]:  # 跳过表头
                cols = [ele.text.strip() for ele in row.find_all('td')]
                #print(cols)
                data.append([ele for ele in cols if ele])  # 过滤掉空值
                #print(data)
            
            # 使用pandas创建DataFrame
            df = pd.DataFrame(data, columns=headers[1:])
            df.insert(loc=0, column=headers[0], value=stock_code)
            
            # 显示数据
            #print(df.head())
            return df
            
            # 可以进行进一步的数据处理和分析
            # ...
        else:
            print(f'Failed to retrieve data, status code: {response.status_code}')

if __name__ == '__main__':
    print(StockCapitalFlows().get_inflow(stock_code='600519'))
    