"""
Rate limiting middleware using Redis

Implements IP-based rate limiting with configurable limits and whitelist support.
"""

import os
import time
import json
from typing import List, Optional
from fastapi import Request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import redis
from redis.exceptions import RedisError


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware for rate limiting requests by IP address.
    
    Uses Redis to track request counts per IP with configurable:
    - Rate limit (requests per second)
    - Whitelisted IPs (no rate limiting)
    """
    
    def __init__(self, app, redis_client: redis.Redis, req_per_sec: int = None, whitelist: List[str] = None):
        super().__init__(app)
        self.redis_client = redis_client
        # Get req_per_sec from environment if not provided
        if req_per_sec is None:
            req_per_sec_env = os.getenv("REQ_PER_SEC")
            if not req_per_sec_env:
                raise ValueError("REQ_PER_SEC must be set in environment variables")
            self.req_per_sec = int(req_per_sec_env)
        else:
            self.req_per_sec = req_per_sec
        self.whitelist = whitelist or []
        
    async def dispatch(self, request: Request, call_next):
        """Process the request and apply rate limiting"""
        
        # Get client IP
        client_ip = self._get_client_ip(request)
        
        # Skip rate limiting for whitelisted IPs
        if client_ip in self.whitelist:
            response = await call_next(request)
            return response
        
        # Check rate limit
        try:
            if not self._check_rate_limit(client_ip):
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "RateLimitExceeded",
                        "message": f"Rate limit exceeded. Maximum {self.req_per_sec} requests per second allowed.",
                        "retry_after": 1
                    },
                    headers={
                        "Retry-After": "1",
                        "X-RateLimit-Limit": str(self.req_per_sec),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(time.time()) + 1)
                    }
                )
        except RedisError as e:
            # If Redis is down, allow the request but log the error
            print(f"Redis error in rate limiter: {e}")
            # Optionally, you could fail closed (deny all) instead of fail open
            
        # Process the request
        response = await call_next(request)
        
        # Add rate limit headers
        if client_ip not in self.whitelist:
            remaining = self._get_remaining_requests(client_ip)
            response.headers["X-RateLimit-Limit"] = str(self.req_per_sec)
            response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
            response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 1)
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """
        Extract client IP from request, checking for proxy headers.
        
        Checks in order:
        1. X-Forwarded-For header (for proxies/load balancers)
        2. X-Real-IP header (nginx)
        3. Direct client connection
        """
        # Check X-Forwarded-For header (most common for proxies)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Take the first IP in the chain (original client)
            return forwarded_for.split(",")[0].strip()
        
        # Check X-Real-IP header (common with nginx)
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()
        
        # Fall back to direct connection IP
        if request.client and request.client.host:
            return request.client.host
        
        # Default if no IP found
        return "unknown"
    
    def _check_rate_limit(self, client_ip: str) -> bool:
        """
        Check if the client has exceeded the rate limit.
        
        Uses Redis to track requests with a sliding window approach.
        Returns True if request is allowed, False if rate limit exceeded.
        """
        try:
            # Create a key for this IP with current second
            current_second = int(time.time())
            key = f"rate_limit:{client_ip}:{current_second}"
            
            # Increment the counter for this second
            count = self.redis_client.incr(key)
            
            # Set expiration to 2 seconds (cleanup old keys)
            if count == 1:
                self.redis_client.expire(key, 2)
            
            # Check if limit exceeded
            return count <= self.req_per_sec
            
        except RedisError:
            # If Redis fails, allow the request (fail open)
            # You could change this to fail closed if preferred
            return True
    
    def _get_remaining_requests(self, client_ip: str) -> int:
        """Get the number of remaining requests for this second"""
        try:
            current_second = int(time.time())
            key = f"rate_limit:{client_ip}:{current_second}"
            count = self.redis_client.get(key)
            
            if count is None:
                return self.req_per_sec
            
            return max(0, self.req_per_sec - int(count))
            
        except RedisError:
            return self.req_per_sec


def parse_whitelist(whitelist_str: str) -> List[str]:
    """
    Parse whitelist from environment variable string.
    
    Supports both comma-separated and JSON array formats:
    - "192.168.1.1,10.0.0.1"
    - '["192.168.1.1", "10.0.0.1"]'
    """
    if not whitelist_str:
        return []
    
    # Try parsing as JSON first
    try:
        parsed = json.loads(whitelist_str)
        if isinstance(parsed, list):
            return [str(ip).strip() for ip in parsed]
    except json.JSONDecodeError:
        pass
    
    # Fall back to comma-separated
    return [ip.strip() for ip in whitelist_str.split(",") if ip.strip()]


def create_redis_client(redis_url: str = None, redis_password: str = None) -> Optional[redis.Redis]:
    """
    Create a Redis client from URL or environment variables.
    
    Args:
        redis_url: Redis connection URL (e.g., redis://host:port)
        redis_password: Redis password
        
    Returns:
        Redis client or None if connection fails
    """
    try:
        if redis_url:
            # Parse Redis URL
            if redis_url.startswith("redis://"):
                redis_url = redis_url[8:]  # Remove redis:// prefix
            
            host_port = redis_url.split(":")
            host = host_port[0]
            port = int(host_port[1]) if len(host_port) > 1 else 6379
            
            client = redis.Redis(
                host=host,
                port=port,
                password=redis_password,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
        else:
            # Use default localhost connection
            client = redis.Redis(
                host="localhost",
                port=6379,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
        
        # Test connection
        client.ping()
        return client
        
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        return None