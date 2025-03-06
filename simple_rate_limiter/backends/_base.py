from abc import ABC, abstractmethod

from simple_rate_limiter.rate import Rate


class BaseBackend(ABC):
    @abstractmethod
    def try_acquire(self, rate: Rate, key: str, num_tokens: int) -> int:
        pass

    @abstractmethod
    def try_acquire_all(self, rate: Rate, key: str, num_tokens: int) -> bool:
        pass
