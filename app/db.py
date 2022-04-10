import aioredis

async def connect():
    print("Starting connection to Redis...")
    conn = await aioredis.from_url("redis://redis/0")
    print("Connection to Redis established")
    return conn