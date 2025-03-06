from abc import ABC, abstractmethod
from simple_rate_limiter.rate import Rate


class BaseBackend(ABC):
    @abstractmethod
    def try_acquire(self, rate: Rate, key: str, num_tokens: int) -> int:
        pass

    @abstractmethod
    def try_acquire_all(self, rate: Rate, key: str, num_tokens: int) -> bool:
        pass

    @staticmethod
    def get_allowed(now, num_tokens, rate, record):
        record.sync(rate, now)
        allowed = max(
            min(rate.max_tokens - record.calculate_current_rate(rate, now), num_tokens),
            0,
        )
        return allowed
