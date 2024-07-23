# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/3/29
@log: change log
"""
# cookie = 'BAIDUID=61D17458C811DF0B06467F8750EE21C2:FG=1; ab_sr=1.0.1_NDc4ZjNhNWJlNDk2N2M2MjI2ZGM2MzEwNzZiMGZiYTMyMGMyMzgxNWUxYTY1MjBhZDU5ODJhMWRjYmMxOTY5NWQ5MGI0M2MzMGMwYzQyMmUwZjcxNGQyNGZjZTZjNGJjN2NiODM3N2NlMjQ3YWNkNGJjNWVlNzI4YmI2OGI3NTMyMGE5NmQ0ZDZlZjZiODM1ZTIxNDAzMDYzMjIyZTE3ZQ=='
cookie = 'BAIDUID=883657749CC8B8D669D673902D41EBC5:FG=1;ab_sr=1.0.1_ZDA1MjU4MjQ2MWYwNDQ1M2M5OWNiYWI5YTI1YzhlMzNlYjk5YTlmNTk1YzY2N2NmOTBkZjkwNjE1Yjg5YzUwNmJhZDQ4NmE4ZTMzZDFhZTBjODhjM2Q4MmYzMjg1Y2MzMzgzOWQ2NDI0NDk1YWFlZWEzZmNmZTk1ZTgzMTMzZTNmYjRhYWZjZWJkZDJjOTBmYzFlMGMxNDJkNzZjYWQ4Yg==; Path=/; Domain=baidu.com; Max-Age=7200; HttpOnly; Secure; SameSite=None'

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
