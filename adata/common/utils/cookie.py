# -*- coding: utf-8 -*-
"""
@desc: 获取cookie的工具类
@author: 1nchaos
@time: 2023/5/5
@log: change log
"""
from importlib import resources

from py_mini_racer import py_mini_racer


def ths_cookie(js_path="ths.js"):
    """获取同花顺cookie"""
    js_code = py_mini_racer.MiniRacer()
    js_content = get_file_content_ths(file_path=js_path)
    js_code.eval(js_content)
    return 'v=' + js_code.call("v")+";"


def get_file_content_ths(file_path: str = None) -> str:
    """
    获取 JS 文件的内容
    :param file_path:  JS 文件名
    :return: 文件内容
    """
    with resources.path("adata.common.js", file_path) as f_path:
        with open(f_path) as f:
            file_data = f.read()
        return file_data


if __name__ == '__main__':
    print(ths_cookie())
