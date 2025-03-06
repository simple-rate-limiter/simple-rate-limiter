from simple_rate_limiter.decorator import Decorator
from simple_rate_limiter.mapper import Mapper
from simple_rate_limiter.rate_limiter import RateLimiter


class MyMapper(Mapper):
    @staticmethod
    def key(client: str, bar: list, *args, **kwargs) -> int:
        return client

    @staticmethod
    def tokens(client: str, bar: list, *args, **kwargs) -> int:
        return len(bar)

    @staticmethod
    def preprocess(tokens: int, client: str, bar: list, *args, **kwargs) -> int:
        return client, bar[:tokens], args, kwargs


rl = RateLimiter(max_tokens=3, period=1, backend="memory")

rate_limited = Decorator(rl, MyMapper())
