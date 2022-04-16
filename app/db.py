import aioredis

async def connect():
    print("Starting connection to Redis...")
    conn = await aioredis.from_url("redis://redis/0")
    print("Connection to Redis established")
    return conn

async def get_name():
    redis = await connect()
    name = await redis.get("name")
    name = "No name found" if name is None else str(name, 'utf-8')
    await redis.close()
    return name

async def set_name(name):
    redis = await connect()
    new = await redis.set("name", name)
    await redis.close()
    return new