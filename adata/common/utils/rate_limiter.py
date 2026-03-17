# -*- coding: utf-8 -*-
"""
@desc: 基于域名的请求限流器
@author: 1nchaos
@time: 2026/3/18
@log: 实现基于滑动窗口的域名级请求频率控制
"""

import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, Optional
from urllib.parse import urlparse
import logging

logger = logging.getLogger("adata")


@dataclass
class RateLimitConfig:
    """限流配置数据类"""
    max_requests: int = 30  # 默认每分钟最大请求数
    time_window: int = 60   # 默认时间窗口（秒）
    wait_message: bool = True  # 是否显示等待提示


class DomainRateLimiter:
    """
    基于滑动窗口的域名限流器
    为每个域名维护独立的请求时间窗口
    """
    
    def __init__(self):
        # 域名 -> 请求时间队列 的映射
        self._domain_windows: Dict[str, deque] = {}
        # 域名 -> 限流配置 的映射
        self._domain_configs: Dict[str, RateLimitConfig] = {}
        # 全局默认配置
        self._default_config = RateLimitConfig()
        # 线程锁，保证线程安全
        self._lock = threading.RLock()
    
    def set_domain_config(self, domain: str, max_requests: Optional[int] = None, 
                          time_window: Optional[int] = None) -> None:
        """
        设置特定域名的限流配置
        
        :param domain: 域名，如 "eastmoney.com"
        :param max_requests: 时间窗口内最大请求数，None表示使用默认值
        :param time_window: 时间窗口（秒），None表示使用默认值
        """
        with self._lock:
            if domain not in self._domain_configs:
                self._domain_configs[domain] = RateLimitConfig()
            
            if max_requests is not None:
                self._domain_configs[domain].max_requests = max_requests
            if time_window is not None:
                self._domain_configs[domain].time_window = time_window
            
            logger.info(f"[RateLimiter] 域名 {domain} 限流配置已更新: "
                       f"{self._domain_configs[domain].max_requests}次/"
                       f"{self._domain_configs[domain].time_window}秒")
    
    def set_default_config(self, max_requests: Optional[int] = None,
                           time_window: Optional[int] = None) -> None:
        """
        设置全局默认限流配置
        
        :param max_requests: 默认时间窗口内最大请求数
        :param time_window: 默认时间窗口（秒）
        """
        with self._lock:
            if max_requests is not None:
                self._default_config.max_requests = max_requests
            if time_window is not None:
                self._default_config.time_window = time_window
            
            logger.info(f"[RateLimiter] 默认限流配置已更新: "
                       f"{self._default_config.max_requests}次/"
                       f"{self._default_config.time_window}秒")
    
    def get_domain_config(self, domain: str) -> RateLimitConfig:
        """获取域名的限流配置，如未配置则返回默认配置"""
        with self._lock:
            return self._domain_configs.get(domain, self._default_config)
    
    def _extract_domain(self, url: str) -> str:
        """从URL中提取域名"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            # 移除端口（如果有）
            if ':' in domain:
                domain = domain.split(':')[0]
            return domain
        except Exception:
            return "unknown"
    
    def acquire(self, url: str) -> float:
        """
        尝试获取请求许可，如超限则等待
        
        :param url: 请求的URL
        :return: 实际等待的时间（秒）
        """
        domain = self._extract_domain(url)
        config = self.get_domain_config(domain)
        
        with self._lock:
            # 初始化该域名的请求窗口
            if domain not in self._domain_windows:
                self._domain_windows[domain] = deque()
            
            window = self._domain_windows[domain]
            now = time.time()
            
            # 清理窗口中已过期的请求记录
            cutoff_time = now - config.time_window
            while window and window[0] < cutoff_time:
                window.popleft()
            
            # 检查是否需要等待
            if len(window) >= config.max_requests:
                # 计算需要等待的时间
                oldest_request = window[0]
                wait_time = (oldest_request + config.time_window) - now
                
                if wait_time > 0:
                    if config.wait_message:
                        logger.warning(f"[RateLimiter] 域名 {domain} 请求频率超限 "
                                      f"({config.max_requests}次/{config.time_window}秒), "
                                      f"等待 {wait_time:.2f} 秒...")
                    
                    # 释放锁，等待时间
                    self._lock.release()
                    try:
                        time.sleep(wait_time)
                    finally:
                        self._lock.acquire()
                    
                    # 重新获取当前时间并清理过期记录
                    now = time.time()
                    cutoff_time = now - config.time_window
                    while window and window[0] < cutoff_time:
                        window.popleft()
            
            # 记录本次请求时间
            window.append(now)
            
            return 0.0  # 成功获取许可，无需额外等待
    
    def get_stats(self, domain: Optional[str] = None) -> dict:
        """
        获取限流统计信息
        
        :param domain: 指定域名，None表示返回所有域名统计
        :return: 统计信息字典
        """
        with self._lock:
            if domain:
                if domain not in self._domain_windows:
                    return {"domain": domain, "request_count": 0}
                window = self._domain_windows[domain]
                config = self.get_domain_config(domain)
                now = time.time()
                # 统计窗口内有效请求数
                valid_count = sum(1 for t in window if t > now - config.time_window)
                return {
                    "domain": domain,
                    "request_count": valid_count,
                    "max_requests": config.max_requests,
                    "time_window": config.time_window,
                    "window_size": len(window)
                }
            else:
                return {
                    "domains": list(self._domain_windows.keys()),
                    "configured_domains": list(self._domain_configs.keys()),
                    "default_config": {
                        "max_requests": self._default_config.max_requests,
                        "time_window": self._default_config.time_window
                    }
                }
    
    def reset(self, domain: Optional[str] = None) -> None:
        """
        重置限流器状态
        
        :param domain: 指定域名，None表示重置所有域名
        """
        with self._lock:
            if domain:
                if domain in self._domain_windows:
                    self._domain_windows[domain].clear()
                    logger.info(f"[RateLimiter] 域名 {domain} 限流状态已重置")
            else:
                self._domain_windows.clear()
                logger.info("[RateLimiter] 所有域名限流状态已重置")


# 全局限流器单例
_rate_limiter_instance: Optional[DomainRateLimiter] = None
_instance_lock = threading.Lock()


def get_rate_limiter() -> DomainRateLimiter:
    """获取全局限流器实例（单例模式）"""
    global _rate_limiter_instance
    if _rate_limiter_instance is None:
        with _instance_lock:
            if _rate_limiter_instance is None:
                _rate_limiter_instance = DomainRateLimiter()
    return _rate_limiter_instance


def set_rate_limit(domain: str, max_requests: int = 30, time_window: int = 60) -> None:
    """
    设置特定域名的限流参数（便捷函数）
    
    :param domain: 域名，如 "eastmoney.com"
    :param max_requests: 时间窗口内最大请求数
    :param time_window: 时间窗口（秒）
    
    示例:
        >>> from adata.common.utils.rate_limiter import set_rate_limit
        >>> set_rate_limit("eastmoney.com", max_requests=30, time_window=60)
    """
    limiter = get_rate_limiter()
    limiter.set_domain_config(domain, max_requests=max_requests, time_window=time_window)


def set_default_rate_limit(max_requests: int = 30, time_window: int = 60) -> None:
    """
    设置默认限流参数（便捷函数）
    
    :param max_requests: 默认时间窗口内最大请求数
    :param time_window: 默认时间窗口（秒）
    
    示例:
        >>> from adata.common.utils.rate_limiter import set_default_rate_limit
        >>> set_default_rate_limit(max_requests=20, time_window=60)
    """
    limiter = get_rate_limiter()
    limiter.set_default_config(max_requests=max_requests, time_window=time_window)
    #

def enable_rate_limiter() -> None:
    """
    启用限流器（需要在导入sunrequests之前调用）
    
    示例:
        >>> from adata.common.utils.rate_limiter import enable_rate_limiter
        >>> enable_rate_limiter()
        >>> import adata
    """
    limiter = get_rate_limiter()
    # 设置一个标记，表示限流器已启用
    limiter._enabled = True
    logger.info("[RateLimiter] 请求限流器已启用")


def get_stats(domain: Optional[str] = None) -> dict:
    """
    获取限流统计信息（便捷函数）
    
    :param domain: 指定域名，None表示返回所有域名统计
    :return: 统计信息字典
    """
    limiter = get_rate_limiter()
    return limiter.get_stats(domain)


def reset_rate_limiter(domain: Optional[str] = None) -> None:
    """
    重置限流器状态（便捷函数）
    
    :param domain: 指定域名，None表示重置所有域名
    """
    limiter = get_rate_limiter()
    limiter.reset(domain)
