# AGENTS.md

本文件面向 AI 编码代理（以及新加入的人类贡献者），描述 AData 项目的结构与不可违反的工程约定。
动手改代码前请先读完第 3、4、12 节；新增数据源请直接照第 5 节清单执行。

---

## 1. 项目概览

- **是什么**：AData 是 A 股量化数据 SDK（PyPI 包名 `adata`），专注行情、财务、资金流、舆情数据。
- **核心设计**：*多数据源融合切换*。同一份数据由新浪/腾讯/百度/东方财富/同花顺等多个来源提供，一个源失败自动降级到下一个。
- **对外入口**（必须保持不变）：
  ```python
  adata.stock.info      # 代码、交易日历、概念、指数成分
  adata.stock.market    # K 线、分时、五档、资金流、概念行情
  adata.stock.finance   # 财务三大表核心指标
  adata.stock.index     # 指数计算
  adata.fund            # ETF 信息与行情
  adata.bond            # 可转债代码与行情
  adata.sentiment       # 热榜、北向资金、融资融券、解禁、扫雷
  ```
- **规模**：约 97 个 Python 文件 / 6000 行，业务代码全部在 `adata/` 下。

## 2. 环境与验证命令

```bash
# 依赖：requests pandas beautifulsoup4 py_mini_racer（见 requirements.txt）
python -m venv .venv
.venv/bin/pip install requests pandas beautifulsoup4 py_mini_racer mini-racer

# 语法检查
.venv/bin/python -m compileall -q adata

# 全模块导入检查（必须输出「失败模块: 0 个」）
.venv/bin/python -c "
import importlib, pkgutil, adata
bad = []
for m in pkgutil.walk_packages(adata.__path__, 'adata.'):
    try:
        importlib.import_module(m.name)
    except Exception as e:
        bad.append((m.name, repr(e)))
for name, err in bad:
    print(name, err)
print('失败模块:', len(bad), '个')"

# 格式与 lint（工具需自行安装：pip install black isort pylint）
black --check --line-length 120 adata
isort --check-only --profile black adata
pylint --rcfile=pylintrc adata
```

- **Python 版本**：`setup.py` 声明 3.6–3.12，`pylintrc` 设 `py-version=3.7`。**禁止使用 3.8+ 专属语法**（海象运算符 `:=`、`f"{x=}"`、仅位置参数 `/` 等）。
- **格式基线**：black `line-length = 120`，isort `profile = "black"`。
- `pylintrc` 设 `max-line-length=128`（比 black 宽松，作为兜底）、`fail-under=10.0`，并已关闭 `missing-docstring`、`invalid-name`、`unsubscriptable-object`、`unsupported-assignment-operation`（pandas 误报）。**不要为了过 lint 去改 `pylintrc`**。

## 3. 目录结构与职责

```
adata/
├── __init__.py          # 公开入口：logger / set_logger / proxy / version
├── __version__.py       # 版本元数据（发布前改这里）
├── _logger.py           # 日志实现（内部基础设施，勿导出为新 API）
├── common/
│   ├── base/            # BaseThs（同花顺反爬：cookie + JS 执行）
│   ├── exception/       # handler_null 装饰器、异常文案常量
│   ├── headers/         # 各数据源请求头常量（按域名分文件）
│   ├── js/              # 同花顺 JS 校验脚本（hexin.js / ths.js）
│   └── utils/           # requests 封装、代码/日期工具、cookie、单位换算、雪花 ID
├── stock/
│   ├── cache/           # 交易日历 CSV、全量代码表（随包分发，见 MANIFEST.in）
│   ├── info/            # 代码、概念、指数、财报以外的静态信息
│   ├── finance/         # 三大表
│   ├── index/           # 指数计算
│   └── market/          # 行情类，全部遵循"模板-实现-门面"三层
├── fund/                # 结构同 stock/market
├── bond/                # 结构同 stock/market
└── sentiment/           # 舆情类，多为独立抓取实现
tests/
├── adata_test/          # 人工/联网用例（unittest），断言依赖真实接口返回规模
├── other/ tests/utils/  # 临时脚本，不作为回归依据
```

## 4. 架构契约

### 4.1 三层结构（行情/信息类模块必须遵守）

以股票行情为例：

| 层 | 文件 | 类 | 职责 |
|---|---|---|---|
| 模板层 | `stock_market_template.py` | `StockMarketTemplate` | 定义 `_XXX_COLUMNS` 列名常量；声明方法骨架（`pass`）；提供公共辅助方法 |
| 实现层 | `stock_market_sina.py` 等 | `StockMarketSina` | 只负责"一个数据源"的请求 + 解析，继承模板层 |
| 门面层 | `stock_market.py` | `StockMarket` | 组合多个实现层，按顺序降级，是唯一对外暴露的类 |

- 实现层**不得**被 `adata/__init__.py` 直接导出；用户只应接触门面层。
- 门面层通过**多重继承**聚合多个业务方法（见 `adata/stock/market/__init__.py` 的 `class Market(StockCapitalFlow, ConceptCapitalFlow, StockMarket, ...)`）。
- 每个包在 `__init__.py` 末尾实例化单例：`stock = Stock()`，供 `adata.stock.xxx` 使用。

### 4.2 降级链规则

门面层按"主源 → 备源"顺序调用，**用返回结果是否为空判断降级**，不要用 try/except 包住整段：

```python
df = self.east_market.get_market_min(stock_code=stock_code)
if df.empty:
    df = self.baidu_market.get_market_min(stock_code=stock_code)
return df
```

新增备源时，观察现有顺序的注释（如"其中：百度的接口数据更精准，精确到了股"），不要随意调整优先级。

### 4.3 公开 API 稳定性（硬约束）

- **禁止**修改 `adata.xxx` 下的模块路径、类名、公开方法名、参数名与默认值、返回列名。
- **禁止**给公开方法新增必填参数；新增能力一律用带默认值的关键字参数。
- 内部可自由重构：临时变量、私有方法、实现细节均可调整，但对外行为保持不变。

## 5. 新增一个数据源（标准清单）

1. 在对应目录新建 `xxx_<source>.py`，类名 `Xxx<Source>`，继承 `XxxTemplate`。
2. 复制文件头模板（见 6.1），`@desc` 写数据源名称 + 官网 URL，`@time` 写当天日期。
3. 只实现需要覆盖的方法，其余继承模板层的空实现；返回 `pd.DataFrame` 且列序等于模板层常量。
4. 请求统一走 `from adata.common import requests`，见第 8 节。
5. 方法体使用编号步骤注释：`# 1.请求接口` / `# 2. 判断结果是否正确` / `# 3.解析数据` / `# 4. 封装数据`。
6. 在门面层注册该实现，并按 4.2 的降级顺序接入。
7. 文件末尾加 `if __name__ == '__main__':` 自测块（见 10.1），跑通后删掉调试输出。

### 5.1 新增一个业务方法

1. 先判断它属于哪个业务域（`info` / `market` / `finance` / `sentiment`），不要为单个方法新建顶层包。
2. 在模板层声明方法骨架 + 列常量，再在门面层写降级链。
3. 门面层方法必须带 docstring（中文说明 + `:param:` + `:return:`），因为它是用户唯一看得到的地方。
4. 参数命名与同类方法对齐：`stock_code`、`code_list`、`start_date`、`end_date`、`k_type`、`adjust_type`。
5. 改完跑一遍 `import adata` 与该方法对应的 `__main__` 自测块。

## 6. 编码风格

### 6.1 文件头（所有 `.py` 文件必须包含）

```python
# -*- coding: utf-8 -*-
"""
@desc: 一句话说明 +（可选）数据源 URL
@author: 1nchaos
@time: 2023/06/19
@log: change log
"""
```

- 新建文件 `@author` 保留项目作者，`@time` 用 `YYYY/M/D` 或 `YYYY/MM/DD`（两种历史写法均可，同一文件内一致）。
- 数据源相关文件在 `@desc` 中附上可追溯的接口 URL。

### 6.2 命名

| 对象 | 约定 | 示例 |
|---|---|---|
| 模块 | `snake_case`，与主类一一对应 | `stock_market_sina.py` |
| 类 | `PascalCase`，末尾带数据源 | `StockMarketSina`、`NorthFlow` |
| 公开方法 | `snake_case`，动词开头 | `get_market`、`list_market_current`、`all_code` |
| 私有方法 | 双下划线前缀 | `__market_rank_baidu` |
| 受保护成员 | 单下划线前缀 | `_MARKET_COLUMNS`、`_empty_df` |
| 列名常量 | 类内大写 `_XXX_COLUMNS` | `_MARKET_CURRENT_COLUMNS` |
| 文件名拼写 | 数据源统一用 `baidu` / `east` / `ths` / `sina` / `qq` | — |

- 方法命名保持三类语义：`get_xxx` 单个对象、`list_xxx` 多个代码、`all_xxx` 全量。
- 新代码的列常量统一用**单下划线**（模板层风格）；历史模块的双下划线写法不要动。

### 6.3 导入顺序

标准库 → 第三方 → `adata` 内部，组间空一行（isort black profile）：

```python
import ast
import time

import pandas as pd

from adata._logger import get_logger
from adata.common import requests
from adata.stock.market.stock_market.stock_market_template import StockMarketTemplate
```

### 6.4 注释与文档字符串

- 注释和 docstring **一律中文**，与现有代码保持一致。
- 关键流程用编号注释，全项目已用 200+ 处：`# 1. 请求数据`、`# 2. 解析数据`。
- docstring 用 Sphinx 字段风格：
  ```python
  def get_market(self, stock_code: str = '000001', start_date='1990-01-01'):
      """
      获取单个股票的行情
      :param stock_code: 股票代码
      :param start_date: 开始时间
      :return: k线行情数据，列见 _MARKET_COLUMNS
      """
  ```
- 陷阱、反直觉逻辑、数据源怪癖必须写明原因，不要只写"做了什么"。

### 6.5 禁止模块级副作用

不要在模块顶层执行 `pd.set_option(...)`、发网络请求、读写文件、启动线程。需要全局设置时放进 `if __name__ == '__main__':` 块或由调用方显式触发。

## 7. 数据返回契约

- **一律返回 `pandas.DataFrame`**，不返回 list/dict/None；即使无数据也返回带列名的空表。
- 列名常量定义在模板层类的私有属性上，实现层通过 `self._XXX_COLUMNS` 引用。
- 空结果优先级：
  1. 已有基类辅助方法时用 `self._empty_df(self._MARKET_CURRENT_COLUMNS)`
  2. 否则 `pd.DataFrame(data=[], columns=self._XXX_COLUMNS)`
  3. `return pd.DataFrame()`（无列名）仅存在于历史代码，**新代码不要这样写**
- **单位必须归一到"股 / 元 / %"**：数据源常返回"手""万元"，需在解析时换算（参考 `stock_market_sina.py` 中 `volume * 100`、`amount * 10000`）。
- 市场标识统一取 `SH` / `SZ` / `BJ`，用 `code_utils.get_exchange_by_stock_code(code)`，不要自己切字符串判断。
- 日期列用 `pd.to_datetime(...)` 归一；价格/量列用 `float` / `int` 显式转换。

## 8. 网络请求契约

- **必须**用项目封装，禁止直接用第三方 `requests`。两种写法完全等价（都指向 `sun_requests` 单例），按所在层级选择：
  ```python
  from adata.common import requests                 # 业务模块惯用写法（15 处）
  from adata.common.utils import requests           # 同效（17 处）

  res = requests.request(method='get', url=url, headers=xxx_headers.xxx, proxies={})
  ```
- 仅 `adata/common/utils/sunrequests.py` 内部允许 `import requests`（它就是封装本身）。
- `SunRequests.request` 已内建：默认 `timeout=15s`、最多尝试 3 次（`times=3`，含首次）、重试间隔 1588ms。
  - **不要**再显式传 `timeout=15`（冗余）；确需覆盖时才传。
  - **4xx（429 除外）不会重试**，直接返回响应，调用方需自行判断 `status_code`。
  - 需要限速时传 `wait_time=<毫秒>`（每次请求前的休眠），不要自己写 `time.sleep`。
- `proxies={}` 表示"本次请求显式关闭代理"，用于绕过 `adata.proxy()` 设置的全局代理；不传则走全局配置。批量抓取、限流敏感接口建议显式传。
- 请求头从 `adata.common.headers.<source>_headers` 取，不要写死 UA。
- **严禁**对远端内容使用 `eval` / `exec`。解析 JS 字面量用 `ast.literal_eval`，并先做括号配平截取（参考 `stock_market_qq.py` 的 `__parse_bar_text`）。
- 数据源返回 403/401 说明被限流，**应立即放弃该源并降级**，不要逐页重试空转。

## 9. 异常与日志

- **禁止 `bare except`**（`except:`）。必须写明异常类型，如 `except (ValueError, IndexError, KeyError):`。
- 兜底最外层用 `@handler_null` 装饰器：捕获异常、记 warning（含堆栈）、返回空 DataFrame。用于**对外取数方法**的顶层，不要滥用在内层逻辑。
- 取数方法内部若需捕获，用精确类型 + 日志，不允许静默 `pass`。
- 日志统一入口：
  ```python
  from adata._logger import get_logger
  logger = get_logger(__name__)
  ```
- 日志级别约定：
  - `debug`：单条记录解析失败、可跳过的问题
  - `warning`：数据源降级、请求被拒、接口结构异常
  - `error`：不应发生且需人工介入的问题
- **禁止在库代码里 `print`**；仅 `if __name__ == '__main__':` 调试块允许。
- 公开日志接口是 `adata.logger` / `adata.set_logger()` / `adata.set_logger(logging.DEBUG)`，`set_logger` 幂等，不要重复注册 handler。

## 10. 测试

### 10.1 文件内自测（项目惯例）

每个数据源文件末尾保留：

```python
if __name__ == '__main__':
    print(StockMarketSina().list_market_current(code_list=['000001', '600905']))
    exit()
```

### 10.2 用例目录

- `tests/adata_test/`：unittest 用例，**依赖真实网络与数据源规模**（如断言 `len(df) > 300`）。改代码后应至少跑通改动涉及模块的用例。
- `tests/other/`、`tests/utils/` 是历史脚本，不作为回归标准。
- 因数据源波动导致失败时，**不要**通过放宽断言、删除用例、加 `skip` 来"修复"，应在说明中明确指出这是外部数据源问题。

## 11. 版本与发布

1. 修改 `adata/__version__.py` 的 `VERSION = (主, 次, 修订)` 三元组，`__version__` 由其自动生成，不要手写。
2. 在 `HISTORY.md` 顶部按 `x.y.z (YYYY-MM-DD)` 格式追加条目，用"新增/修复/优化"分条。
3. 新增非 `.py` 资源（CSV、JS）时，同步更新 `MANIFEST.in` 与 `setup.py` 的 `include_package_data`，否则打包后缺失。
4. 本项目以 `dev` 为主干分支，发布合并到 `main`。

## 12. 红线清单（禁止事项）

1. 不要修改任何 `adata.xxx` 公开路径、类名、方法签名或返回列名。
2. 不要重命名以下历史拼写（会破坏用户代码）：`adata/stock/market/concepth_market/`、类 `ConceptMarketEase`、测试文件 `makert_test.py`。
3. 不要使用 `eval` / `exec` 处理网络返回内容。
4. 不要在库代码中 `print`，不要保留 `bare except`。
5. 不要在模块顶层产生副作用（改 pandas 全局配置、发请求、写文件）。
6. 不要绕过 `adata.common.utils.requests` 直接调用第三方 `requests`。
7. 不要未经要求新增第三方依赖；确有需要时同步 `requirements.txt` 与 `setup.py`。
8. 不要为了让 lint/测试通过而放宽 `pylintrc`、删除用例或修改断言。
9. 不要往 `adata/stock/cache/` 塞临时抓取文件；该目录只放 `code.csv` 与 `calendar/*.csv` 这类随包分发的正式资源。

## 13. 已知陷阱

- **循环导入**：`adata/common/__init__.py` 用了 `from .utils import *`，任何子模块反向 `import adata` 都有风险。跨包基础设施（如 logger）必须放在 `adata/_logger.py`，只依赖标准库。
- **`handler_null` 会吞掉异常**：返回空表但不再抛错，排查线上问题必须先打开日志（`adata.set_logger(logging.DEBUG)`）。
- **数据源不可达是常态**：东财、百度会因 IP 限流返回 403 或直接断开连接。写代码时默认"随时可能失败"，必须有降级与超时。
- **pandas 版本差异**：项目声明支持 pandas 0.22+，实际已在 3.x 上验证。避免使用已废弃 API（`append`、`inplace` 与链式赋值组合等）。
- **同花顺反爬**：`BaseThs` 需要动态 cookie 与 JS 校验（`common/js/*.js` 由 `py_mini_racer` 执行），修改相关代码前先确认 `wencai_hexin_v()` 仍可用。
- **包内资源定位**：`adata/stock/cache/*.csv` 与 `adata/common/js/*.js` 随包分发，必须按 `__file__` 定位。注意历史函数 `get_code_csv_path()` 用 `os.path.join(os.getcwd(), os.path.dirname(__file__))`，**实际依赖运行时工作目录**，从其他目录调用会读不到文件。新代码一律用 `os.path.dirname(os.path.abspath(__file__))`，不要模仿旧写法。
