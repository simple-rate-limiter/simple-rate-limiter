from abc import ABC, abstractmethod
from simple_rate_limiter.rate import Rate


class BaseBackend(ABC):

    def try_acquire(self, rate: Rate, key: str, num_tokens: int) -> int:
        return self._try_acquire(rate, key, num_tokens, require_all=False)

    def try_acquire_all(self, rate: Rate, key: str, num_tokens: int) -> bool:
        return self._try_acquire(rate, key, num_tokens, require_all=True)

    @abstractmethod
    def _try_acquire(self, rate: Rate, key: str, num_tokens: int, require_all: bool) -> int | bool:
        pass

    @staticmethod
    def get_allowed(now, num_tokens, rate, record):
        record.sync(rate, now)
        allowed = max(
            min(rate.max_tokens - record.calculate_current_rate(rate, now), num_tokens),
            0,
        )
        return allowed
