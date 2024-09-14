import aioredis
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Redis URL from environment variables
REDIS_URL = os.getenv('REDIS_URL')

# Create a Redis client
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

async def set_cache(key: str, value: str, expire: int = 3600):
    """
    Set a value in the Redis cache with an optional expiration time.

    Args:
        key (str): The cache key.
        value (str): The value to cache.
        expire (int): Expiration time in seconds (default is 3600 seconds).
    """
    await redis_client.set(key, value, ex=expire)

async def get_cache(key: str) -> str:
    """
    Get a value from the Redis cache by its key.

    Args:
        key (str): The cache key.

    Returns:
        str: The cached value, or None if not found.
    """
    return await redis_client.get(key)

async def delete_cache(key: str):
    """
    Delete a value from the Redis cache by its key.

    Args:
        key (str): The cache key.
    """
    await redis_client.delete(key)


import asyncio

async def test_cache():
    await set_cache("test_key", "test_value")
    value = await get_cache("test_key")
    print(f"Cached value for 'test_key': {value}")
    await delete_cache("test_key")

if __name__ == "__main__":
    asyncio.run(test_cache())
