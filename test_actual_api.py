
import sys
import time

print("=" * 80)
print("adata API 真实限流测试 - 30次/分钟")
print("=" * 80)

print("\n正在初始化 adata 模块...")

try:
    import adata
    from adata.common.utils.rate_limiter import (
        enable_rate_limit,
        get_rate_limiter
    )
    print("✓ adata 模块导入成功")
except Exception as e:
    print("✗ adata 模块导入失败:", str(e))
    sys.exit(1)

print("\n" + "=" * 80)
print("[配置说明]")
print("=" * 80)
print("  限流配置: 30次/分钟 (真实60秒窗口)")
print("  测试接口: adata.stock.market.get_market()")
print("  股票代码: 000001")

enable_rate_limit(True)
limiter = get_rate_limiter()

print("\n" + "=" * 80)
print("[测试 1] 20次请求 - 不应触发限流")
print("=" * 80)

start1 = time.time()
results1 = []
success_count1 = 0

for i in range(20):
    try:
        print("  [请求 %2d] 发送请求..." % (i + 1))
        res_df = adata.stock.market.get_market(
            stock_code='000001',
            k_type=1,
            start_date='2026-03-17'
        )
        results1.append(res_df)
        success_count1 = success_count1 + 1
        if res_df is not None and len(res_df) > 0:
            print("    成功 - 返回 %d 条数据" % len(res_df))
        else:
            print("    成功 - 返回空数据")
    except Exception as e:
        print("    失败: %s" % str(e))

elapsed1 = time.time() - start1

print("\n✓ 测试 1 完成")
print("  总耗时: %.2f秒" % elapsed1)
print("  成功请求: %d/20" % success_count1)
print("  结果: " + ("通过" if success_count1 == 20 and elapsed1 < 60.0 else "异常"))

print("\n" + "=" * 80)
print("[测试 2] 40次请求 - 真实60秒限流")
print("=" * 80)
print("\n提示: 此测试将使用真实60秒限流配置")
print("      前30次请求会快速完成，第31次开始触发等待")
print("      整个测试将需要至少60秒完成，请耐心等待...")

input("\n按回车键开始测试 2 (Ctrl+C 可取消)...")

start2 = time.time()
results2 = []
success_count2 = 0
wait_triggered = False

for i in range(40):
    try:
        print("\n  [请求 %2d] 发送请求..." % (i + 1))
        res_df = adata.stock.market.get_market(
            stock_code='000001',
            k_type=1,
            start_date='2026-03-17'
        )
        results2.append(res_df)
        success_count2 = success_count2 + 1
        if res_df is not None and len(res_df) > 0:
            print("    成功 - 返回 %d 条数据" % len(res_df))
        else:
            print("    成功 - 返回空数据")
    except Exception as e:
        print("    失败: %s" % str(e))

elapsed2 = time.time() - start2

print("\n" + "=" * 80)
print("✓ 测试 2 完成")
print("=" * 80)
print("  总耗时: %.2f秒" % elapsed2)
print("  成功请求: %d/40" % success_count2)
print("  结果: " + ("通过" if elapsed2 >= 60.0 else "未触发限流"))

print("\n" + "=" * 80)
print("所有测试完成！")
print("=" * 80)

