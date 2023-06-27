# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/6/2
@log: change log
"""
import datetime

if __name__ == '__main__':
    start_date = '2020-01-01'
    years = []
    if not start_date:
        years.append('last')
    else:
        current_year = datetime.datetime.now().year
        start_year = datetime.datetime.strptime(start_date, "%Y-%m-%d").year
        while start_year <= current_year:
            years.append(start_year - 1)
            start_year += 1
        if current_year not in years:
            years.append(current_year)
    print(years)
