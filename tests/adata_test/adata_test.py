# -*- coding: utf-8 -*-
import time
import unittest

import requests
from HTMLTestRunner import HTMLTestRunner

import adata

if __name__ == "__main__":
    version = adata.version()
    proxy_url = "http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=100017&port=11&pack=326296&ts=0&ys=0&cs=0&lb=6&sb=0&pb=4&mr=1&regions="
    # ip = requests.get(proxy_url).text
    # adata.proxy(is_proxy=True, proxy_url=proxy_url)
    # 会识别出所在目录中，文件名字为test*.py格式的文件
    # defaultTestLoader测试加载器：包含加载测试用例的方法;使用discover()方法来自动识别并添加测试用例(多个)
    suite = unittest.defaultTestLoader.discover("", '*_test.py')
    # 生成一个本地时间 格式如20220413091429，年月时时分秒
    time_str = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
    # 生成的报告的名字和目录
    filename = f"./AData-{version}自动化测试报告-" + time_str + ".html"
    # 打开这个文件
    fn = open(filename, 'wb')
    # 测试报告的标题与描述 实例化HTMLTestRunner()，参数stream是文件
    runner = HTMLTestRunner(stream=fn, title=f'AData-{version}自动化测试报告', description='测试用例执行情况')
    # 运行测试套件
    runner.run(suite)
    # 关闭文件流，不关的话生成的报告是空的
    fn.close()
