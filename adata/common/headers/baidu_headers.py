# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/3/29
@log: change log
"""
cookie = 'BAIDUID=5D6B41AD5BE03619A214B371970EB643:FG=1; BIDUPSID=72A958B07427F9F9CB3F63FD8B6C6565; PSTM=1723618492; ZFY=USOzWykRABpB9kTNtM29hNaXpj:AfNf0O65YLgmVy2Fg:C; H_PS_PSSID=60274_60359_60599_60607_60664_60677_60674_60694_60709; BA_HECTOR=252hagaka4alah2g81a4818036oger1jdasff1u; PSINO=6; delPer=0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; ab_sr=1.0.1_M2I1MThhZjNiZTMwYzJiZTA1N2RiOTAzZGI4OGZiZTZiOGZiY2RmZTQyY2YxZTlmYWFkZjExODhjZmY1MGM1N2M1YjBlZjhkMzNmZmY3ZjVkYmJmZDE0ODM1MTg5NTQ3MDJkZTFiMGM4MTViMWU2YmYxYjU3ZmVlZGM5NDVhOWIzOWQwMTBmMzBmNTk4NWQ2MmMwYjQ5MDdhNjI2MDY3OA=='
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
