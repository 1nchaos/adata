# -*- coding: utf-8 -*-
"""
@desc: readme
@author: yinchao
@time: 2024/7/23
@log: change log
"""
import requests

# cookie = 'BAIDUID=61D17458C811DF0B06467F8750EE21C2:FG=1; ab_sr=1.0.1_NDc4ZjNhNWJlNDk2N2M2MjI2ZGM2MzEwNzZiMGZiYTMyMGMyMzgxNWUxYTY1MjBhZDU5ODJhMWRjYmMxOTY5NWQ5MGI0M2MzMGMwYzQyMmUwZjcxNGQyNGZjZTZjNGJjN2NiODM3N2NlMjQ3YWNkNGJjNWVlNzI4YmI2OGI3NTMyMGE5NmQ0ZDZlZjZiODM1ZTIxNDAzMDYzMjIyZTE3ZQ=='
cookie = 'BAIDUID=61D17458C811DF0B06467F8750EE21C2:FG=1; ab_jid=4612ca84faa72ab407fd722d950fc31fe1d1; ab_bid=faa72ab407fd722d950fc31fe1d217e49c55; ab_sr=1.0.1_YjY5ZGYxMzM0NTc3ZmYwNjE4OTE2ZTNiMDEzMzEwN2JmMWRjMjBhOWY0Njc4YjlhNmM5M2ViMjZiZmNmYWI1MTU0NzQ3YmU0MjJmYTM2YWNiZjEyYjE1ODdjMjc0MDQxNWU4ZmI0MmNjZWFhODRlZDAyMjIxNmE0YzdkNmUyYjI5M2Q3NjE3OTc2ZDliNDIxYWUyMWRhYmVhODZjZjlhZA==; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598'

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
params = {
    '_o': 'https://gushitong.baidu.com'
}
response = requests.post(url='https://miao.baidu.com/abdr', params=params)
# response = requests.get('https://gushitong.baidu.com/stock/ab-300059')
print(response.cookies)
