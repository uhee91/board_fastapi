from typing import Optional
# from aioredis import Redis, from_url
from redis import Redis, from_url


class RedisCache:

    def __init__(self):
        self.redis_cache: Optional[Redis] = None

    def init_cache(self):
        # self.redis_cache = from_url("redis://127.0.0.1:6379", decode_responses=True)  # Connecting to database
        self.redis_cache = from_url("redis://board_fastapi-redis-1:6379", decode_responses=True)  # Connecting to database

    def keys(self, pattern):
        return self.redis_cache.keys(pattern)

    def set(self, key, value):
        return self.redis_cache.set(key, value)

    def get(self, key):
        return self.redis_cache.get(key)

    def expire(self, key, timeout):
        return self.redis_cache.expire(key, timeout)

    def hset(self, name, key, value):
        return self.redis_cache.hset(name, key, value)

    def hget(self, name, key):
        return self.redis_cache.hget(name, key)

    def hdel(self, name, key):
        return self.redis_cache.hdel(name, key)

    def delete(self, name):
        return self.redis_cache.delete(name)

    def close(self):
        self.redis_cache.close()
        # self.redis_cache.wait_closed()


redis_cache = RedisCache()
