# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/3/29
@log: change log
"""
cookie = 'BAIDUID=FB17C036F6F79E647798CCDBF10D0A3A:FG=1; BIDUPSID=72A958B07427F9F9CB3F63FD8B6C6565; PSTM=1721131010; BA_HECTOR=21252ka18l04ah0g0k8k84a4brl9d31j9co021u; ZFY=RDRljN0vytzynS1BEIuC:A79HiL:AOmQZYkiXI4VbDvTo:C; ab_sr=1.0.1_ZDg2NTdmYTk5MjE3MDhiMzNhMDRiZDQyNzJhOWQwZTcwMDkzMjU2YzFiOTNiNjZlODU1ODcwYTMzMjRlYjVkODlhY2UwZWFkYmM1MmM1MGUxMDVmYWM4YWMyYTdmOWFjN2JiZWQyMjUzMDVkMmNhNzg1ZjIzNjk1ZDlmZjQyZTdmNjkwNjFmMDk0YjEzY2Y1NTkxNzI2ZWQ2NGY3MzEzNw=='

json_headers = {
    'Host': 'finance.pae.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
    'Accept': 'application/vnd.finance-web.v1+json',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/josn',
    'Origin': 'https://gushitong.baidu.com',
    'Connection': 'keep-alive',
    'Referer': 'https://gushitong.baidu.com/',
    'Cookie': cookie
}

text_headers = {
    'Host': 'gushitong.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': cookie,
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}
