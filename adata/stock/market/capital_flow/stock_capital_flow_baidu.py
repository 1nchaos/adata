# -*- coding: utf-8 -*-
"""
@desc: 股票资金流向

东方财富：个股
https://data.eastmoney.com/zjlx/000001.html
https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?cb=jQuery112303663243111530894_1718714074308&lmt=0&klt=101&fields1=f1%2Cf2%2Cf3%2Cf7&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61%2Cf62%2Cf63%2Cf64%2Cf65&ut=b2884a393a59ad64002292a3e90d46a5&secid=1.600519&_=1718714074309

@author: 1nchaos
@time: 2024/6/7
@log: change log
"""

from adata.stock.market.capital_flow.stock_capital_flow_template import StockCapitalFlowTemplate


class StockCapitalFlowBaidu(StockCapitalFlowTemplate):

    def get_capital_flow_min(self, stock_code: str = '000001'):
        """
        获取单个股票的今日分时资金流向
        :param stock_code: 股票代码
        :return: 当日分钟资金流向
        """
        url = f"https://finance.pae.baidu.com/vapi/v1/fundflow?finance_type=stock&fund_flow_type=&" \
              f"type=stock&market=ab&name=%E4%B8%9C%E6%96%B9%E8%B4%A2%E5%AF%8C&" \
              f"code={stock_code}&belongs=stocklevelone&finClientType=pc"
        pass

    def get_capital_flow(self, stock_code: str = '000001'):
        """
        获取单个股票的资金流向-日度
        目前只有120天的数据
        :param stock_code: 股票代码
        :return: 资金流向-日度
        """
        date = '20240430'
        url = f"https://finance.pae.baidu.com/vapi/v1/fundsortlist?" \
              f"code={stock_code}&market=ab&finance_type=stock&tab=day&" \
              f"from=history&date={date}&rn=20&finClientType=pc"
        pass


if __name__ == '__main__':
    print(StockCapitalFlowBaidu().get_capital_flow_min(stock_code='000001'))
    print(StockCapitalFlowBaidu().get_capital_flow(stock_code='000001'))
