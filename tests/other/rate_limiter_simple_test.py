# -*- coding: utf-8 -*-
"""
Simple test for rate limiter - standalone version
"""
import sys
import time
import threading
from collections import deque
from dataclasses import dataclass
from typing import Dict, Optional
from urllib.parse import urlparse

# Copy the rate limiter code here for standalone testing

@dataclass
class RateLimitConfig:
    max_requests: int = 30
    time_window: int = 60
    wait_message: bool = True


class DomainRateLimiter:
    def __init__(self):
        self._domain_windows: Dict[str, deque] = {}
        self._domain_configs: Dict[str, RateLimitConfig] = {}
        self._default_config = RateLimitConfig()
        self._lock = threading.RLock()

    def set_domain_config(self, domain: str, max_requests: Optional[int] = None,
                          time_window: Optional[int] = None) -> None:
        with self._lock:
            if domain not in self._domain_configs:
                self._domain_configs[domain] = RateLimitConfig()
            if max_requests is not None:
                self._domain_configs[domain].max_requests = max_requests
            if time_window is not None:
                self._domain_configs[domain].time_window = time_window

    def get_domain_config(self, domain: str) -> RateLimitConfig:
        with self._lock:
            return self._domain_configs.get(domain, self._default_config)

    def _extract_domain(self, url: str) -> str:
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            if ':' in domain:
                domain = domain.split(':')[0]
            return domain
        except Exception:
            return "unknown"

    def acquire(self, url: str) -> float:
        domain = self._extract_domain(url)
        config = self.get_domain_config(domain)

        with self._lock:
            if domain not in self._domain_windows:
                self._domain_windows[domain] = deque()

            window = self._domain_windows[domain]
            now = time.time()

            cutoff_time = now - config.time_window
            while window and window[0] < cutoff_time:
                window.popleft()

            if len(window) >= config.max_requests:
                oldest_request = window[0]
                wait_time = (oldest_request + config.time_window) - now

                if wait_time > 0:
                    self._lock.release()
                    try:
                        time.sleep(wait_time)
                    finally:
                        self._lock.acquire()

                    now = time.time()
                    cutoff_time = now - config.time_window
                    while window and window[0] < cutoff_time:
                        window.popleft()

            window.append(now)
            return 0.0

    def get_stats(self, domain: str) -> dict:
        with self._lock:
            if domain not in self._domain_windows:
                return {"domain": domain, "request_count": 0}
            window = self._domain_windows[domain]
            config = self.get_domain_config(domain)
            now = time.time()
            valid_count = sum(1 for t in window if t > now - config.time_window)
            return {
                "domain": domain,
                "request_count": valid_count,
                "max_requests": config.max_requests,
                "time_window": config.time_window,
            }


print("=" * 60)
print("Testing Rate Limiter Basic Functionality")
print("=" * 60)

# Test 1: Basic rate limiting
print("\nTest 1: Basic rate limiting (2 requests per 2 seconds)")
limiter = DomainRateLimiter()
limiter.set_domain_config('test.com', max_requests=2, time_window=2)

# First 2 requests should pass immediately
start = time.time()
limiter.acquire('http://test.com/api')
limiter.acquire('http://test.com/api')
elapsed1 = time.time() - start
print(f"  First 2 requests took: {elapsed1:.2f}s (expected < 0.5s)")

# 3rd request should wait
start = time.time()
limiter.acquire('http://test.com/api')
elapsed2 = time.time() - start
print(f"  3rd request took: {elapsed2:.2f}s (expected > 1s)")

if elapsed1 < 0.5 and elapsed2 > 1.0:
    print("  PASSED!")
else:
    print("  FAILED!")

# Test 2: Different domains are independent
print("\nTest 2: Different domains are independent")
limiter2 = DomainRateLimiter()
limiter2.set_domain_config('a.com', max_requests=1, time_window=10)
limiter2.set_domain_config('b.com', max_requests=10, time_window=10)

start = time.time()
limiter2.acquire('http://a.com/api')
elapsed_a1 = time.time() - start

start = time.time()
limiter2.acquire('http://b.com/api')
elapsed_b1 = time.time() - start

print(f"  a.com 1st request: {elapsed_a1:.2f}s")
print(f"  b.com 1st request: {elapsed_b1:.2f}s")

if elapsed_a1 < 0.1 and elapsed_b1 < 0.1:
    print("  PASSED!")
else:
    print("  FAILED!")

# Test 3: Default config
print("\nTest 3: Default config")
limiter3 = DomainRateLimiter()
config = limiter3.get_domain_config('unknown.com')
print(f"  Default max_requests: {config.max_requests} (expected 30)")
print(f"  Default time_window: {config.time_window} (expected 60)")

if config.max_requests == 30 and config.time_window == 60:
    print("  PASSED!")
else:
    print("  FAILED!")

# Test 4: Stats
print("\nTest 4: Stats tracking")
limiter4 = DomainRateLimiter()
limiter4.set_domain_config('stats.com', max_requests=5, time_window=60)

for _ in range(3):
    limiter4.acquire('http://stats.com/api')

stats = limiter4.get_stats('stats.com')
print(f"  Request count: {stats['request_count']} (expected 3)")
print(f"  Max requests: {stats['max_requests']} (expected 5)")

if stats['request_count'] == 3 and stats['max_requests'] == 5:
    print("  PASSED!")
else:
    print("  FAILED!")

# Test 5: Simulate the 30 requests/minute scenario
print("\nTest 5: Simulate 30 requests/minute limit")
limiter5 = DomainRateLimiter()
limiter5.set_domain_config('api.com', max_requests=30, time_window=60)

# Send 30 requests quickly
start = time.time()
for i in range(30):
    limiter5.acquire('http://api.com/data')
elapsed_30 = time.time() - start
print(f"  30 requests took: {elapsed_30:.2f}s (should be quick)")

# 31st request should trigger wait (but we'll wait less for testing)
# Actually, let's use a smaller window for faster testing
limiter5.set_domain_config('api2.com', max_requests=5, time_window=3)

start = time.time()
for i in range(5):
    limiter5.acquire('http://api2.com/data')
elapsed_5 = time.time() - start
print(f"  First 5 requests to api2.com took: {elapsed_5:.2f}s")

start = time.time()
limiter5.acquire('http://api2.com/data')  # 6th request
elapsed_6th = time.time() - start
print(f"  6th request to api2.com took: {elapsed_6th:.2f}s (should wait ~3s)")

if elapsed_5 < 1.0 and elapsed_6th > 2.0:
    print("  PASSED!")
else:
    print("  FAILED!")

print("\n" + "=" * 60)
print("All basic tests completed!")
print("=" * 60)
