
# API 限流中间件使用说明

## 概述

这是一个可插拔的 API 请求限流中间件，用于保护股票行情数据采集系统免受 IP 封禁、API 配额耗尽或服务商限制。

## 核心特性

- 基于域名的独立频率控制
- 默认 30次/分钟 的限流策略
- 支持自定义特定域名的限流阈值
- 运行时动态调整参数，无需重启
- 超限请求给出明确的等待提示
- 线程安全
- 最小侵入性，对现有业务代码零修改

## 文件位置

- 核心限流模块: `adata/common/utils/rate_limiter.py`
- 集成限流的请求封装: `adata/common/utils/sunrequests.py`

## 快速开始

### 1. 启用限流（一行代码）

```python
from adata.common.utils.rate_limiter import enable_rate_limit

# 启用全局限流
enable_rate_limit(True)
```

### 2. 配置限流参数

```python
from adata.common.utils.rate_limiter import set_domain_limit, set_default_limit

# 设置默认限流（例如：改为 50次/分钟）
set_default_limit(50, 60)

# 设置特定域名的限流（例如：新浪财经 20次/分钟）
set_domain_limit("finance.sina.com.cn", 20, 60)

# 设置东方财富 40次/分钟
set_domain_limit("push2.eastmoney.com", 40, 60)
```

### 3. 完整使用示例

```python
# 导入模块
from adata.common.utils.rate_limiter import enable_rate_limit, set_domain_limit
from adata.common.utils.sunrequests import sun_requests

# 步骤1: 启用限流
enable_rate_limit(True)

# 步骤2: 配置特定域名的限流（可选）
set_domain_limit("api.example.com", 25, 60)

# 步骤3: 正常使用请求，自动限流
url = "https://api.example.com/stock/data"
response = sun_requests.request(url=url)
print(response.text)
```

## API 参考

### `enable_rate_limit(enable=True)`
启用或禁用全局限流功能。

**参数:**
- `enable` (bool): True 启用，False 禁用，默认 True

**返回:**
- SunRequests 实例

---

### `set_domain_limit(domain, limit, window=60)`
设置特定域名的限流阈值。

**参数:**
- `domain` (str): 域名（例如 "api.example.com"）
- `limit` (int): 允许的请求次数
- `window` (int): 时间窗口（秒），默认 60 秒

---

### `set_default_limit(limit, window=60)`
设置全局默认限流阈值。

**参数:**
- `limit` (int): 默认允许的请求次数
- `window` (int): 时间窗口（秒），默认 60 秒

---

### `get_rate_limiter()`
获取限流器单例实例，用于高级操作。

**返回:**
- RateLimiter 实例

## 工作原理

### 限流算法
采用**滑动窗口算法**，精确控制请求频率：

1. 记录每个请求的时间戳
2. 清理时间窗口外的过期请求
3. 检查当前窗口内的请求数是否超限
4. 如超限，计算需要等待的时间

### 域名隔离
每个域名拥有独立的限流配置和请求记录，互不干扰。

### 线程安全
使用 `threading.RLock` 保证多线程环境下的安全性。

## 限流提示

当请求超限时时，会在控制台输出提示信息：

```
[RateLimit] 域名 api.example.com 已达到 30 次/60 秒限制，等待 15.32 秒...
```

## 性能测试

### 测试场景1: 20次请求（不触发限流）

期望结果：20次请求快速完成，无等待

```python
from adata.common.utils.rate_limiter import get_rate_limiter

limiter = get_rate_limiter()
limiter.set_default_limit(30, 60)
url = "https://test.example.com/api"

for i in range(20):
    wait = limiter.acquire(url)
    assert wait == 0  # 无需等待
```

### 测试场景2: 40次请求（触发限流）

期望结果：前30次快速完成，第31次开始触发等待

```python
from adata.common.utils.rate_limiter import get_rate_limiter

limiter = get_rate_limiter()
limiter.set_default_limit(30, 60)
url = "https://test.example.com/api"

wait_triggered = False
for i in range(40):
    wait = limiter.acquire(url)
    if wait &gt; 0:
        wait_triggered = True

assert wait_triggered == True  # 应该触发等待
```

## 兼容性说明

- 默认不启用限流，完全向后兼容
- 限流器模块导入失败时不影响现有功能
- 支持 Python 3.6+

## 禁用限流

如需临时禁用限流：

```python
from adata.common.utils.rate_limiter import enable_rate_limit

# 禁用限流
enable_rate_limit(False)
```

## 注意事项

1. 限流是基于内存的，进程重启后计数会重置
2. 多进程场景下，每个进程有独立的限流计数
3. 建议根据实际 API 服务商的限制合理配置阈值
4. 限流不会中止请求，只是延迟执行

