# AData 字典表

> 整个项目API的数据字典，按照模块层级分类命名，描述尽量精简，以便进行查阅。

## 股票-stock

### 一、基本信息-Info

#### 1.股票代码信息（info）

| 字段       | 类型   | 注释   | 说明                        |
| ---------- | ------ | ------ | --------------------------- |
| stock_code | string | 代码   | 600001                      |
| short_name | string | 简称   | 中国平安                    |
| exchange   | string | 交易所 | SH:上交；BJ：北交；SZ：深交 |

#### 2.概念指数信息（index-concept）

| 字段         | 类型   | 注释     | 说明                                                |
| ------------ | ------ | -------- | --------------------------------------------------- |
| name         | string | 名称     | 物联网                                              |
| index_code   | string | 指数代码 | 同花顺的概念指数代码是：8开头；例：885312           |
| concept_code | string | 概念代码 | 同花顺的概念代码是：3开头；例：309061；注意不要混淆 |
| source       | string | 来源     |                                                     |

#### 3.指数代码信息（index）

| 字段       | 类型   | 注释     | 说明   |
| ---------- | ------ | -------- | ------ |
| short_name | string | 指数简称 |        |
| index_code | string | 指数代码 |        |
| source     | string | 来源     | 同花顺 |

#### 11.交易日历

| 字段         | 类型 | 注释                           | 说明           |
| ------------ | ---- | ------------------------------ | -------------- |
| trade_date   | date | 交易日                         | 2023-05-20     |
| trade_status | int  | 交易状态：0.非交易日；1.交易日 | 1              |
| day_week     | int  | 一周第几天                     | 从星期天开始的 |

### 二、行情信息-Market

#### 1.分红（dividend）

| 字段             | 类型   | 注释       | 说明                         |
| ---------------- | ------ | ---------- | ---------------------------- |
| stock_code       | string | 代码       | 600001                       |
| report_date      | date   | 公告日     | 1990-01-01                   |
| dividend_plan    | string | 分红方案   | 10股派3.00元，10股转赠5.00股 |
| ex_dividend_date | date   | 除权除息日 | 1990-01-01                   |



#### 2.行情（market）

##### 2.1k线

| 字段           | 类型    | 注释       | 说明                                      |
| -------------- | ------- | ---------- | ----------------------------------------- |
| stock_code     | string  | 代码       | 600001                                    |
| trade_time     | time    | 交易时间   | 1990-01-01 00:00:00；分时图使用具体的时间 |
| trade_date     | date    | 交易日期   | 1990-01-01                                |
| open           | decimal | 开盘价(元) | 9.98                                      |
| close          | decimal | 收盘价(元) | 9.98                                      |
| high           | decimal | 最高价(元) | 9.98                                      |
| low            | decimal | 最低价(元) | 9.98                                      |
| volume         | decimal | 成交量(股) | 64745722                                  |
| amount         | decimal | 成交额(元) | 934285179.00                              |
| change         | decimal | 涨跌额(元) | -0.02                                     |
| change_pct     | decimal | 涨跌幅(%)  | -0.16                                     |
| turnover_ratio | decimal | 换手率(%)  | 0.38                                      |
| pre_close      | decimal | 昨收(元)   | 10.00                                     |

##### 2.2分时

| 字段       | 类型    | 注释       | 说明                                      |
| ---------- | ------- | ---------- | ----------------------------------------- |
| stock_code | string  | 代码       | 600001                                    |
| trade_time | time    | 交易时间   | 1990-01-01 00:00:00；分时图使用具体的时间 |
| trade_date | date    | 交易日期   | 1990-01-01                                |
| price      | decimal | 价格(元)   | 9.98                                      |
| avg_price  | decimal | 平均价(元) | 9.98                                      |
| change     | decimal | 涨跌额(元) | -0.02                                     |
| change_pct | decimal | 涨跌幅(%)  | -0.16                                     |
| volume     | decimal | 成交量(股) | 64745722                                  |
| amount     | decimal | 成交额(元) | 934285179.00                              |

##### 2.3实时

| 字段       | 类型    | 注释         | 说明     |
| ---------- | ------- | ------------ | -------- |
| stock_code | string  | 代码         | 600001   |
| short_name | string  | 简称         | 平安银行 |
| price      | decimal | 当前价格(元) | 12.36    |
| change     | decimal | 涨跌额(元)   | 0.02     |
| change_pct | decimal | 涨跌幅(%)    | 0.16     |
| volume     | decimal | 成交量(股)   | 34452500 |
| amount     | decimal | 成交额(元)   |          |

#### 3.概念&指数行情（concept market）&（index market）

概念和指数字典表一致

##### 3.1k线

| 字段       | 类型    | 注释       | 说明                                      |
| ---------- | ------- | ---------- | ----------------------------------------- |
| index_code | string  | 代码       | 886041                                    |
| trade_time | time    | 交易时间   | 1990-01-01 00:00:00；分时图使用具体的时间 |
| trade_date | date    | 交易日期   | 1990-01-01                                |
| open       | decimal | 开盘价(元) | 9.98                                      |
| close      | decimal | 收盘价(元) | 9.98                                      |
| high       | decimal | 最高价(元) | 9.98                                      |
| low        | decimal | 最低价(元) | 9.98                                      |
| volume     | decimal | 成交量(股) | 64745722                                  |
| amount     | decimal | 成交额(元) | 934285179.00                              |
| change     | decimal | 涨跌额(元) | -0.02                                     |
| change_pct | decimal | 涨跌幅(%)  | -0.16                                     |

##### 3.2分时

| 字段       | 类型    | 注释       | 说明                                      |
| ---------- | ------- | ---------- | ----------------------------------------- |
| index_code | string  | 代码       | 886041                                    |
| trade_time | time    | 交易时间   | 1990-01-01 00:00:00；分时图使用具体的时间 |
| trade_date | date    | 交易日期   | 1990-01-01                                |
| price      | decimal | 现价(元)   | 9.98                                      |
| avg_price  | decimal | 均价价(元) | 9.98                                      |
| high       | decimal | 最高价(元) | 9.98                                      |
| low        | decimal | 最低价(元) | 9.98                                      |
| volume     | decimal | 成交量(股) | 64745722                                  |
| amount     | decimal | 成交额(元) | 934285179.00                              |
| change     | decimal | 涨跌额(元) | -0.02                                     |
| change_pct | decimal | 涨跌幅(%)  | -0.16                                     |

##### 3.3实时

| 字段       | 类型    | 注释       | 说明                                |
| ---------- | ------- | ---------- | ----------------------------------- |
| index_code | string  | 代码       | 886041                              |
| trade_time | time    | 交易时间   | 1990-01-01 00:00:00；返回当前的时间 |
| trade_date | date    | 交易日期   | 1990-01-01                          |
| open       | decimal | 开盘价(元) | 9.98                                |
| price      | decimal | 现价(元)   | 9.98                                |
| high       | decimal | 最高价(元) | 9.98                                |
| low        | decimal | 最低价(元) | 9.98                                |
| volume     | decimal | 成交量(股) | 64745722                            |
| amount     | decimal | 成交额(元) | 934285179.00                        |

## 债券-Bond

### 一、基本信息-Info

#### 1.可转换债券代码信息（info）

| 字段          | 类型    | 注释         | 说明            |
| ------------- | ------- | ------------ | --------------- |
| bond_code     | string  | 债券代码     | 123197          |
| bond_name     | string  | 债券名称     | 光力转债        |
| stock_code    | string  | 股票代码     | 300480          |
| short_name    | string  | 股票简称     | 光力科技        |
| sub_date      | date    | 申购日期     | 2023-05-08      |
| issue_amount  | decimal | 发行金额(元) | 400000000.00000 |
| listing_date  | date    | 上市日期     | 2023-05-29      |
| expire_date   | date    | 到期日期     | 2029-05-08      |
| convert_price | decimal | 转换价格(元) | 21.460          |

## 基金-ETF

### 一、基本信息-Info

#### 1.场内可交易etf（info）

| 字段       | 类型    | 注释         | 说明              |
| ---------- | ------- | ------------ | ----------------- |
| fund_code  | string  | 基金代码     | 159001            |
| short_name | string  | 基金简称     | 易方达保证金货币a |
| net_value  | decimal | 最新净值     | 1.1234            |
| net_date   | date    | 最新净值日期 | 2023-06-05        |
| exchange   | string  | 交易所       | SH，SZ            |

## 舆情

#### 1.股票解禁

| 字段       | 类型    | 注释             | 说明             |
| ---------- | ------- | ---------------- | ---------------- |
| stock_code | string  | 股票代码         | 300539           |
| short_name | string  | 股票简称         | 横河精密         |
| lift_date  | date    | 解禁日期         | 1.1234           |
| volume     | decimal | 解禁股数(股)     | 2023-06-05       |
| amount     | decimal | 当前解禁市值(元) | 根据当前价格计算 |
| ratio      | decimal  | 占总股本比例(%)  | 0.36             |
| price      | decimal | 当前价格(元)     | 13.14            |

### 更新记录

| 相关版本 | 更新日期 | 更新内容 | 备注 |
| -------- | -------- | -------- | ---- |

