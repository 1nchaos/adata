# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/6/2
@log: change log
"""
import os


def get_csv_path(year):
    cur_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return fr"{cur_path}/{year}.csv"


years = [2004, 2005, 2006, 2007, 2008, 2009,
         2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019,
         2020, 2021, 2022, 2023, 2024]
