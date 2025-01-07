# -*- coding: utf-8 -*-
"""
@desc: 交易日历测试用例
@author: 1nchaos
"""
import unittest
import pandas as pd
import adata

class TradeCalendarTest(unittest.TestCase):
    """交易日历测试类"""

    def test_trade_calendar_structure(self):
        """测试交易日历数据结构"""
        for year in range(2000, 2026):
            with self.subTest(year=year):
                df = adata.stock.info.trade_calendar(year=year)
                
                # 验证返回类型
                self.assertIsInstance(df, pd.DataFrame, "返回类型应该是 DataFrame")
                
                # 验证必要的列是否存在
                required_columns = ["trade_date", "trade_status", "day_week"]
                for col in required_columns:
                    self.assertIn(col, df.columns, f"缺少必要的列: {col}")
                
                # 验证数据类型
                self.assertEqual(df["trade_date"].dtype, "object", f"trade_date 类型错误: {df['trade_date'].dtype}, year={year}")
                self.assertEqual(df["trade_status"].dtype, "int64", f"trade_status 类型错误: {df['trade_status'].dtype}, year={year}")
                self.assertEqual(df["day_week"].dtype, "int64", f"day_week 类型错误: {df['day_week'].dtype}, year={year}")

    def test_trade_calendar_values(self):
        """测试交易日历数据值"""
        # test_years = [2000, 2010, 2020, 2023, 2024, 2025]
        for year in range(2000, 2025):
            with self.subTest(year=year):
                df = adata.stock.info.trade_calendar(year=year)
                
                # 验证数据值范围
                self.assertTrue(df["trade_status"].isin([0, 1]).all(), "trade_status 值不在 [0,1] 范围内")
                self.assertTrue(df["day_week"].between(1, 7).all(), "day_week 值不在 [1,7] 范围内")
                
                # 验证日期格式和年份
                date_format = r'^\d{4}-\d{2}-\d{2}$'
                self.assertTrue(df["trade_date"].str.match(date_format).all(), "trade_date 格式错误")
                self.assertTrue(df["trade_date"].str.startswith(str(year)).all(), 
                              f"trade_date 年份与输入年份 {year} 不匹配")

if __name__ == '__main__':
    unittest.main() 