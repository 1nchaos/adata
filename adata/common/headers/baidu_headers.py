# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/3/29
@log: change log
"""
cookie = 'BAIDUID=61D17458C811DF0B06467F8750EE21C2:FG=1; BIDUPSID=72A958B07427F9F9CB3F63FD8B6C6565; PSTM=1721814995; H_PS_PSSID=60236_60273_60359_60468_60492_60499_60524; BA_HECTOR=0kal00ak2k84ak00858421a090v4co1jaeckm1u; ZFY=NChHwmWaGLn3NooySpSMtsO8KVHih:A9FSqxJgYQRfv0:C; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; PSINO=6; ab_sr=1.0.1_ZmU0ZWQyY2I0ZTNjZGU1ZTVmZjQ4Zjg1ODQwNTE0ODYzNDdjNTVlMmFkMDkxNzBkZWM5MjBmMTIxMDAwZGEyMjUxYWU5ODQyMTg5YjIwZWY4YWFkNTlmOWVhOWQzMDI0ZDcwNWMwNWIyZjQwZWI1YzQ5MzA0MjZkNjc1MjY3NTljZTgwNjhkMTIwMmYwODQ1NGUyYTZkZjY4ZmU4MDliNg=='
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
