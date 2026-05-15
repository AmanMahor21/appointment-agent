
from src.db.redis import redis
from src.config import settings
from rich import print


async def rate_limiter(user_id: str):
    key = f"rate:telegram:{user_id}"
    limit = settings.rate_limit
    window = settings.rate_limit_window
    print(limit, window, 'rate limit settings')

    current_req = await redis.incr(key)
    print(
        f"User {user_id} has made {current_req} requests in the current window.")

    if current_req == 1:
        await redis.expire(key, window)
    print(current_req <= limit, 'rate limit check result')

    return current_req <= limit
