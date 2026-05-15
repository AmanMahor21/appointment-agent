from src.config import settings
from upstash_redis.asyncio import Redis

redis = Redis(
    url=settings.upstash_redis_rest_url,
    token=settings.upstash_redis_rest_token
)
