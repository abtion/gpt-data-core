import redis


class RedisClient(redis.Redis):
    def __init__(self, host: str, port: str, password: str):
        super().__init__(
            host=host,
            port=port,
            password=password,
        )
