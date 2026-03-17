
import sys
import time

print("=" * 80)
print("adata API 限流测试 - 30次/10秒 (快速验证版)")
print("=" * 80)

print("\n正在初始化 adata 模块...")

try:
    import adata
    from adata.common.utils.rate_limiter import (
        enable_rate_limit,
        get_rate_limiter,
        set_default_limit
    )
    print("✓ adata 模块导入成功")
except Exception as e:
    print("✗ adata 模块导入失败:", str(e))
    sys.exit(1)

print("\n" + "=" * 80)
print("[配置说明]")
print("=" * 80)
print("  限流配置: 30次/10秒 (快速验证)")
print("  真实配置: 30次/60秒 (生产环境)")
print("  测试接口: adata.stock.market.get_market()")
print("  股票代码: 000001")

enable_rate_limit(True)
limiter = get_rate_limiter()
set_default_limit(30, 10)

print("\n" + "=" * 80)
print("[测试] 40次请求 - 验证限流功能")
print("=" * 80)
print("\n提示: 使用30次/10秒配置快速验证")
print("      前30次请求会快速完成，第31次开始触发等待")
print("      整个测试将需要约10秒完成")

start = time.time()
results = []
success_count = 0
wait_triggered = False

for i in range(40):
    try:
        print("\n  [请求 %2d] 发送请求..." % (i + 1))
        res_df = adata.stock.market.get_market(
            stock_code='000001',
            k_type=1,
            start_date='2026-03-16'
        )
        results.append(res_df)
        success_count = success_count + 1
        if res_df is not None and len(res_df) > 0:
            print("    成功 - 返回 %d 条数据" % len(res_df))
            print("    数据示例:")
            print("      %s" % str(res_df.head(2)))
        else:
            print("    成功 - 返回空数据")
    except Exception as e:
        print("    失败: %s" % str(e))

elapsed = time.time() - start

print("\n" + "=" * 80)
print("✓ 测试完成")
print("=" * 80)
print("  总耗时: %.2f秒" % elapsed)
print("  成功请求: %d/40" % success_count)
print("  结果: " + ("通过（限流生效）" if elapsed >= 8.0 else "未触发限流"))

print("\n" + "=" * 80)
print("说明")
print("=" * 80)
print("要测试真实的60秒限流，请修改代码:")
print("  set_default_limit(30, 10)  ->  set_default_limit(30, 60)")
print("\n或使用 test_actual_api.py 文件进行真实60秒测试")

print("\n" + "=" * 80)

