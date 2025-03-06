class RateLimiter:
    def __init__(self, max_tokens, period, backend):
        self.max_tokens = max_tokens
        self.period = period
        self.backend = backend

    def try_acquire(self, key: str, num_tokens: int = 1) -> int:
        pass

    def try_acquire_all(self, key, num_tokens: int = 1):
        pass
