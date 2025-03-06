from simple_rate_limiter.mapper import Mapper
from simple_rate_limiter.rate_limiter import RateLimiter


class Decorator:
    def __init__(self, rate_limiter: RateLimiter, rl_mapper: Mapper):
        self.rate_limiter = rate_limiter
        self.rl_mapper = rl_mapper
        self.registered_functions: dict[str, callable] = {}

    def __call__(self, function, *args, **kwargs):
        def wrapped(*args, **kwargs):
            key = self.rl_mapper.key(*args, **kwargs)
            tokens = self.rl_mapper.tokens(*args, **kwargs)
            if tokens > self.rate_limiter.try_acquire():
                raise
            if self.rate_limiter.batched:
                args, kwargs = self.rl_mapper.preprocess(*args, **kwargs)

            return function(*args, **kwargs)

        return wrapped
