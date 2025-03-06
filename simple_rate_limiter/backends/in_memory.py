from simple_rate_limiter.backends.base import BaseBackend


class InMemoryBackend(BaseBackend):
    def __init__(self):
        self.storage = {}

    def try_acquire(self, key: str, num_tokens: int) -> int:
        pass

    def try_acquire_all(self, key: str, num_tokens: int) -> bool:
        pass
