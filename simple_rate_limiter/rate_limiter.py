from simple_rate_limiter.backends._base import BaseBackend
from simple_rate_limiter.rate import Rate


class RateLimiter:
    def __init__(self, rate: Rate, backend: BaseBackend):
        self.rate = rate
        self.backend = backend

    def try_acquire(self, key: str, num_tokens: int = 1) -> int:
        return self.backend.try_acquire(self.rate, key, num_tokens)

    def try_acquire_all(self, key, num_tokens: int = 1):
        return self.backend.try_acquire_all(self.rate, key, num_tokens)
