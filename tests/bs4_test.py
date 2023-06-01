# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/5/8
@log: change log
"""

from bs4 import BeautifulSoup

if __name__ == '__main__':
    html = '''<div class="m-pager" id="m-page">
                    &nbsp;<a class="cur" page="1" href="javascript:void(0)">1</a>&nbsp;&nbsp;<a class="changePage" page="2" href="javascript:void(0);">2</a>&nbsp;&nbsp;<a class="changePage" page="3" href="javascript:void(0);">3</a>&nbsp;&nbsp;<a class="changePage" page="4" href="javascript:void(0);">4</a>&nbsp;&nbsp;<a class="changePage" page="5" href="javascript:void(0);">5</a>&nbsp;&nbsp;<a class="changePage" page="2" href="javascript:void(0);">下一页</a><a class="changePage" page="10" href="javascript:void(0);">尾页</a><span class="page_info">1/10</span>
                </div>'''

    soup = BeautifulSoup(html, 'html.parser')

    # 获取总页数
    page_info = soup.find('span', {'class': 'page_info'}).text
    total_pages = int(page_info.split("/")[1])

    print(total_pages)  # 输出: 10

if __name__ == '__main__':
    html_str = '<td><a href="http://q.10jqka.com.cn/zs/detail/code/1A0002/" target="_blank">Ａ股指数</a></td>'

    soup = BeautifulSoup(html_str, 'html.parser')
    a_tag = soup.find('a')
    href = a_tag['href']
    code = href.split('/')[-2]

    print(code)
