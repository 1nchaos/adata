# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/6/2
@log: change log
"""
import os


def get_code_csv_path():
    cur_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return fr"{cur_path}/code.csv"
