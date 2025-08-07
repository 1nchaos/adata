# -*- coding: utf-8 -*-
"""
@desc: 
@author: 1nchaos
@time:2025/8/7
@log: 
"""
import os


def get_all_concept_code_east_csv_path():
    cur_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return fr"{cur_path}/all_concept_code_east.csv"


def get_all_code_csv_path():
    cur_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return fr"{cur_path}/all_code.csv"
