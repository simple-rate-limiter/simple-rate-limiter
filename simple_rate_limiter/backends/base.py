from abc import ABC, abstractmethod


class BaseBackend(ABC):
    @abstractmethod
    def try_acquire(self, key: str, num_tokens: int) -> int:
        pass

    @abstractmethod
    def try_acquire_all(self, key: str, num_tokens: int) -> bool:
        pass
