# -*- coding: utf-8 -*-
"""
@desc: 限流器使用示例
@author: 1nchaos
@time: 2026/3/18
@log: 演示如何使用adata的请求限流功能
"""

"""
============================================
AData 请求限流功能使用指南
============================================

功能概述:
---------
AData 现在内置了基于域名的请求限流功能，可以有效防止因高频请求导致的：
- IP被封禁
- API配额耗尽
- 服务商限制

核心特性:
---------
1. 默认30次/分钟的保守策略
2. 支持按域名独立配置限流参数
3. 运行时动态调整，无需重启
4. 对现有代码零侵入
5. 超限请求给出明确的等待提示

使用方法:
---------
"""

# ============================================================
# 示例1: 基本使用（使用默认限流配置）
# ============================================================
def demo_basic_usage():
    """
    基本使用示例
    只需正常导入adata，限流器会自动生效（默认30次/分钟）
    """
    import adata

    # 限流器默认已启用，无需额外配置
    # 查询股票行情，会自动应用限流
    df = adata.stock.market.get_market(
        stock_code='000001',
        k_type=1,
        start_date='2026-03-17'
    )
    print(df)


# ============================================================
# 示例2: 自定义特定域名的限流参数
# ============================================================
def demo_custom_domain_limit():
    """
    为特定数据源设置自定义限流参数
    """
    import adata

    # 为东方财富接口设置更严格的限制：20次/分钟
    adata.rate_limit("eastmoney.com", max_requests=20, time_window=60)

    # 为新浪接口设置更宽松的限制：60次/分钟
    adata.rate_limit("sina.com.cn", max_requests=60, time_window=60)

    # 后续对这些域名的请求会自动应用相应的限流策略
    df = adata.stock.market.get_market(
        stock_code='000001',
        k_type=1,
        start_date='2026-03-17'
    )
    print(df)


# ============================================================
# 示例3: 修改默认限流参数
# ============================================================
def demo_default_limit():
    """
    修改全局默认限流参数
    """
    import adata

    # 设置默认限制为20次/分钟（对所有未单独配置的域名生效）
    adata.rate_limit_default(max_requests=20, time_window=60)

    # 现在所有请求都会使用这个更保守的默认策略


# ============================================================
# 示例4: 禁用/启用限流器
# ============================================================
def demo_toggle_limiter():
    """
    临时禁用或启用限流器
    """
    import adata

    # 禁用限流器（例如在内部网络或测试环境）
    adata.rate_limit_disable()

    # 执行大量请求...（不会触发限流等待）

    # 重新启用限流器
    adata.rate_limit_enable()


# ============================================================
# 示例5: 查看限流统计信息
# ============================================================
def demo_stats():
    """
    查看限流统计信息
    """
    import adata

    # 查看所有域名的统计
    all_stats = adata.rate_limit_stats()
    print("所有域名统计:", all_stats)

    # 查看特定域名的统计
    domain_stats = adata.rate_limit_stats("eastmoney.com")
    print("东方财富域名统计:", domain_stats)


# ============================================================
# 示例6: 重置限流器状态
# ============================================================
def demo_reset():
    """
    重置限流器状态
    """
    import adata

    # 重置特定域名的限流状态
    adata.rate_limit_reset("eastmoney.com")

    # 重置所有域名的限流状态
    adata.rate_limit_reset()


# ============================================================
# 示例7: 实际测试限流效果
# ============================================================
def demo_test_rate_limit():
    """
    测试限流效果
    预期：请求40次应该至少需要等待1分钟（因为每30次需要等待60秒窗口）
    """
    import time
    import adata

    # 重置限流器
    adata.rate_limit_reset()

    # 设置限流：30次/分钟
    adata.rate_limit_default(max_requests=30, time_window=60)

    print("开始测试限流效果...")
    print("配置: 30次/分钟")
    print("=" * 60)

    # 测试20次请求（在限制内，应该很快）
    print("\n测试1: 20次请求（在30次限制内）")
    start = time.time()
    for i in range(20):
        try:
            df = adata.stock.market.get_market(
                stock_code='000001',
                k_type=1,
                start_date='2026-03-17'
            )
            if (i + 1) % 5 == 0:
                print(f"  已完成 {i + 1}/20 次请求")
        except Exception as e:
            print(f"  第 {i + 1} 次请求异常: {e}")

    elapsed_20 = time.time() - start
    print(f"  20次请求完成，用时: {elapsed_20:.2f} 秒")

    # 测试40次请求（超过限制，应该触发等待）
    print("\n测试2: 40次请求（超过30次限制）")
    start = time.time()
    for i in range(40):
        try:
            df = adata.stock.market.get_market(
                stock_code='000001',
                k_type=1,
                start_date='2026-03-17'
            )
            if (i + 1) % 10 == 0:
                elapsed_so_far = time.time() - start
                print(f"  已完成 {i + 1}/40 次请求，累计用时: {elapsed_so_far:.2f} 秒")
        except Exception as e:
            print(f"  第 {i + 1} 次请求异常: {e}")

    elapsed_40 = time.time() - start
    print(f"  40次请求完成，总用时: {elapsed_40:.2f} 秒")

    print("\n" + "=" * 60)
    print("测试结论:")
    print(f"  - 20次请求用时 {elapsed_20:.2f} 秒（预期 < 30秒）")
    print(f"  - 40次请求用时 {elapsed_40:.2f} 秒（预期 > 30秒，因为触发了限流等待）")
    print("=" * 60)


# ============================================================
# 示例8: 推荐配置（生产环境）
# ============================================================
def demo_production_config():
    """
    生产环境推荐配置
    """
    import adata

    # 重置限流器
    adata.rate_limit_reset()

    # 设置保守的默认策略
    adata.rate_limit_default(max_requests=30, time_window=60)

    # 为常用数据源设置特定策略
    # 东方财富 - 较严格
    adata.rate_limit("eastmoney.com", max_requests=30, time_window=60)
    adata.rate_limit("push2his.eastmoney.com", max_requests=30, time_window=60)
    adata.rate_limit("push2.eastmoney.com", max_requests=30, time_window=60)

    # 新浪财经 - 较宽松
    adata.rate_limit("hq.sinajs.cn", max_requests=60, time_window=60)

    # 腾讯财经 - 中等
    adata.rate_limit("qt.gtimg.cn", max_requests=40, time_window=60)

    # 百度股市通 - 中等
    adata.rate_limit("finance.pae.baidu.com", max_requests=40, time_window=60)

    print("生产环境限流配置已应用")
    print("统计信息:", adata.rate_limit_stats())


if __name__ == '__main__':
    print(__doc__)

    # 运行示例7来测试限流效果
    print("\n" + "=" * 60)
    print("运行限流效果测试")
    print("=" * 60)

    # 注意：这个测试会实际发送HTTP请求，耗时较长
    # 如需运行，请取消下面的注释
    # demo_test_rate_limit()

    # 运行生产环境配置示例
    demo_production_config()
