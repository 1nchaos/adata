# -*- coding: utf-8 -*-
"""
@desc: 限流器测试用例
@author: 1nchaos
@time: 2026/3/18
@log: 测试基于域名的请求限流功能
"""

import time
import unittest

import adata
from adata.common.utils.rate_limiter import get_rate_limiter, DomainRateLimiter


class TestRateLimiter(unittest.TestCase):
    """限流器单元测试"""

    def setUp(self):
        """每个测试前重置限流器"""
        adata.rate_limit_reset()

    def test_domain_rate_limiter_basic(self):
        """测试限流器基本功能"""
        limiter = DomainRateLimiter()
        
        # 设置测试域名限制：2次/3秒
        limiter.set_domain_config("test.com", max_requests=2, time_window=3)
        
        # 前2次请求应该立即通过
        start = time.time()
        limiter.acquire("http://test.com/api")
        limiter.acquire("http://test.com/api")
        elapsed = time.time() - start
        
        # 前2次应该几乎不等待
        self.assertLess(elapsed, 0.5, "前2次请求应该立即通过")
        
    def test_domain_rate_limiter_wait(self):
        """测试限流器等待功能"""
        limiter = DomainRateLimiter()
        
        # 设置测试域名限制：2次/2秒
        limiter.set_domain_config("test.com", max_requests=2, time_window=2)
        
        # 先发送2次请求
        limiter.acquire("http://test.com/api")
        limiter.acquire("http://test.com/api")
        
        # 第3次请求应该等待
        start = time.time()
        limiter.acquire("http://test.com/api")
        elapsed = time.time() - start
        
        # 应该等待至少1秒（因为窗口是2秒，但前面2次请求几乎同时发送）
        self.assertGreaterEqual(elapsed, 1.0, "第3次请求应该等待至少1秒")

    def test_different_domains_independent(self):
        """测试不同域名限流独立"""
        limiter = DomainRateLimiter()
        
        # 设置不同域名的限制
        limiter.set_domain_config("a.com", max_requests=1, time_window=10)
        limiter.set_domain_config("b.com", max_requests=10, time_window=10)
        
        # a.com 第1次
        start = time.time()
        limiter.acquire("http://a.com/api")
        elapsed_a1 = time.time() - start
        
        # b.com 第1次（应该不等待）
        start = time.time()
        limiter.acquire("http://b.com/api")
        elapsed_b1 = time.time() - start
        
        # a.com 第2次（应该等待）
        start = time.time()
        limiter.acquire("http://a.com/api")
        elapsed_a2 = time.time() - start
        
        self.assertLess(elapsed_a1, 0.1)
        self.assertLess(elapsed_b1, 0.1)
        self.assertGreaterEqual(elapsed_a2, 9.0, "a.com第2次请求应该等待")

    def test_default_config(self):
        """测试默认配置"""
        limiter = DomainRateLimiter()
        
        # 未配置的域名应该使用默认配置
        config = limiter.get_domain_config("unknown.com")
        self.assertEqual(config.max_requests, 30)
        self.assertEqual(config.time_window, 60)

    def test_stats(self):
        """测试统计功能"""
        limiter = DomainRateLimiter()
        limiter.set_domain_config("stats.com", max_requests=5, time_window=60)
        
        # 发送3次请求
        for _ in range(3):
            limiter.acquire("http://stats.com/api")
        
        stats = limiter.get_stats("stats.com")
        self.assertEqual(stats["request_count"], 3)
        self.assertEqual(stats["max_requests"], 5)


class TestRateLimiterIntegration(unittest.TestCase):
    """限流器集成测试（使用实际adata接口）"""

    def setUp(self):
        """每个测试前重置限流器"""
        adata.rate_limit_reset()

    def test_20_requests_within_limit(self):
        """
        测试20次请求（在30次/分钟限制内，应该不等待或极少等待）
        
        预期：20次请求应该在较短时间内完成（< 10秒）
        """
        print("\n=== 测试20次请求（在限制内）===")
        
        # 设置限流：30次/分钟
        adata.rate_limit_default(max_requests=30, time_window=60)
        
        start_time = time.time()
        success_count = 0
        
        for i in range(20):
            try:
                # 使用东方财富接口查询股票行情
                df = adata.stock.market.get_market(
                    stock_code='000001', 
                    k_type=1, 
                    start_date='2026-03-17'
                )
                if not df.empty:
                    success_count += 1
                if (i + 1) % 5 == 0:
                    print(f"  已完成 {i + 1}/20 次请求")
            except Exception as e:
                print(f"  第 {i + 1} 次请求异常: {e}")
        
        elapsed = time.time() - start_time
        print(f"  20次请求完成，用时: {elapsed:.2f} 秒")
        print(f"  成功次数: {success_count}/20")
        
        # 20次请求应该在较短时间内完成（网络延迟 + 处理时间）
        # 正常情况下应该 < 30秒
        self.assertLess(elapsed, 60, "20次请求应该在一分钟内完成")
        self.assertGreaterEqual(success_count, 15, "至少15次请求应该成功")

    def test_40_requests_exceeds_limit(self):
        """
        测试40次请求（超过30次/分钟限制，应该触发限流等待）
        
        预期：40次请求应该至少需要等待1分钟（因为每30次需要等待60秒窗口）
        """
        print("\n=== 测试40次请求（超过限制）===")
        
        # 设置限流：30次/分钟
        adata.rate_limit_default(max_requests=30, time_window=60)
        
        start_time = time.time()
        success_count = 0
        
        for i in range(40):
            try:
                df = adata.stock.market.get_market(
                    stock_code='000001', 
                    k_type=1, 
                    start_date='2026-03-17'
                )
                if not df.empty:
                    success_count += 1
                if (i + 1) % 10 == 0:
                    elapsed_so_far = time.time() - start_time
                    print(f"  已完成 {i + 1}/40 次请求，用时: {elapsed_so_far:.2f} 秒")
            except Exception as e:
                print(f"  第 {i + 1} 次请求异常: {e}")
        
        elapsed = time.time() - start_time
        print(f"  40次请求完成，总用时: {elapsed:.2f} 秒")
        print(f"  成功次数: {success_count}/40")
        
        # 40次请求，每30次需要等待60秒，所以至少应该等待约30-60秒
        # 加上网络和处理时间，总时间应该 > 30秒
        self.assertGreater(elapsed, 30, "40次请求应该触发限流等待，总时间应该超过30秒")
        self.assertGreaterEqual(success_count, 30, "至少30次请求应该成功")

    def test_domain_specific_limit(self):
        """
        测试特定域名限流配置
        
        为eastmoney.com设置更严格的限制
        """
        print("\n=== 测试特定域名限流配置 ===")
        
        # 设置默认限制较宽松
        adata.rate_limit_default(max_requests=100, time_window=60)
        
        # 为eastmoney.com设置更严格的限制：5次/10秒
        adata.rate_limit("eastmoney.com", max_requests=5, time_window=10)
        
        start_time = time.time()
        
        # 发送8次请求
        for i in range(8):
            try:
                df = adata.stock.market.get_market(
                    stock_code='000001', 
                    k_type=1, 
                    start_date='2026-03-17'
                )
                elapsed_so_far = time.time() - start_time
                print(f"  第 {i + 1} 次请求完成，累计用时: {elapsed_so_far:.2f} 秒")
            except Exception as e:
                print(f"  第 {i + 1} 次请求异常: {e}")
        
        elapsed = time.time() - start_time
        print(f"  8次请求完成，总用时: {elapsed:.2f} 秒")
        
        # 8次请求，每5次需要等待10秒，所以至少应该等待约5秒
        self.assertGreater(elapsed, 5, "超过5次请求应该触发限流等待")

    def test_rate_limit_disable_enable(self):
        """测试禁用和启用限流"""
        print("\n=== 测试禁用/启用限流 ===")
        
        # 先禁用限流
        adata.rate_limit_disable()
        
        # 设置很严格的限制（如果启用会触发）
        adata.rate_limit_default(max_requests=1, time_window=60)
        
        start_time = time.time()
        
        # 发送3次请求（如果限流启用，第2次就会等待）
        for i in range(3):
            try:
                df = adata.stock.market.get_market(
                    stock_code='000001', 
                    k_type=1, 
                    start_date='2026-03-17'
                )
                print(f"  第 {i + 1} 次请求完成")
            except Exception as e:
                print(f"  第 {i + 1} 次请求异常: {e}")
        
        elapsed_disabled = time.time() - start_time
        print(f"  禁用限流时3次请求用时: {elapsed_disabled:.2f} 秒")
        
        # 重新启用限流
        adata.rate_limit_enable()
        adata.rate_limit_reset()  # 重置状态
        
        start_time = time.time()
        
        # 再次发送3次请求（这次应该触发限流）
        for i in range(3):
            try:
                df = adata.stock.market.get_market(
                    stock_code='000001', 
                    k_type=1, 
                    start_date='2026-03-17'
                )
                print(f"  第 {i + 1} 次请求完成")
            except Exception as e:
                print(f"  第 {i + 1} 次请求异常: {e}")
        
        elapsed_enabled = time.time() - start_time
        print(f"  启用限流时3次请求用时: {elapsed_enabled:.2f} 秒")
        
        # 禁用限流时应该更快
        self.assertLess(elapsed_disabled, elapsed_enabled, 
                       "禁用限流时请求应该更快完成")


class TestRateLimiterAPI(unittest.TestCase):
    """测试限流API接口"""

    def setUp(self):
        """每个测试前重置"""
        adata.rate_limit_reset()

    def test_rate_limit_api(self):
        """测试rate_limit API"""
        # 应该能正常设置而不抛出异常
        adata.rate_limit("test.com", max_requests=10, time_window=30)
        
        # 获取统计信息
        stats = adata.rate_limit_stats("test.com")
        self.assertEqual(stats["max_requests"], 10)
        self.assertEqual(stats["time_window"], 30)

    def test_rate_limit_default_api(self):
        """测试rate_limit_default API"""
        adata.rate_limit_default(max_requests=50, time_window=120)
        
        stats = adata.rate_limit_stats()
        self.assertEqual(stats["default_config"]["max_requests"], 50)
        self.assertEqual(stats["default_config"]["time_window"], 120)

    def test_rate_limit_stats_api(self):
        """测试rate_limit_stats API"""
        # 获取所有域名统计
        stats = adata.rate_limit_stats()
        self.assertIn("domains", stats)
        self.assertIn("default_config", stats)

    def test_rate_limit_reset_api(self):
        """测试rate_limit_reset API"""
        # 发送一些请求
        limiter = get_rate_limiter()
        limiter.acquire("http://test.com/api")
        limiter.acquire("http://test.com/api")
        
        # 重置前应该有记录
        stats_before = limiter.get_stats("test.com")
        self.assertEqual(stats_before["request_count"], 2)
        
        # 重置
        adata.rate_limit_reset("test.com")
        
        # 重置后应该清零
        stats_after = limiter.get_stats("test.com")
        self.assertEqual(stats_after["request_count"], 0)


def run_quick_tests():
    """运行快速测试（不依赖网络）"""
    print("\n" + "=" * 60)
    print("运行限流器单元测试（快速，不依赖网络）")
    print("=" * 60)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRateLimiter)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


def run_integration_tests():
    """运行集成测试（依赖网络，耗时较长）"""
    print("\n" + "=" * 60)
    print("运行限流器集成测试（依赖网络，耗时较长）")
    print("=" * 60)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRateLimiterIntegration)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


def run_api_tests():
    """运行API测试"""
    print("\n" + "=" * 60)
    print("运行限流器API测试")
    print("=" * 60)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRateLimiterAPI)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == '__main__':
    # 运行所有测试
    run_quick_tests()
    run_api_tests()
    
    # 集成测试可选（因为耗时较长）
    print("\n" + "=" * 60)
    print("是否运行集成测试？(y/n): ", end="")
    try:
        response = input().strip().lower()
        if response == 'y':
            run_integration_tests()
    except EOFError:
        # 非交互式环境，跳过集成测试
        print("非交互式环境，跳过集成测试")
