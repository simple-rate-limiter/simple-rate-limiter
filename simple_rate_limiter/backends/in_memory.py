import datetime as dt
import threading
from collections import defaultdict

from simple_rate_limiter.backends._base import BaseBackend
from simple_rate_limiter.backends.record import Record
from simple_rate_limiter.rate import Rate


class InMemoryBackend(BaseBackend):
    def __init__(self):
        self._storage: dict[str, Record] = {}
        self._locks: dict[str, threading.Lock] = defaultdict(threading.Lock)

    def _try_acquire(self, rate: Rate, key: str, num_tokens: int, require_all: bool) -> int | bool:
        with self._locks[key]:
            now = dt.datetime.now(dt.UTC)
            rec = self._storage.setdefault(key, Record(now, 0, 0))

            if require_all:
                rec.sync(rate, now)  # Only sync when requiring all tokens

            allowed = self.get_allowed(now, num_tokens, rate, rec)

            if require_all and allowed != num_tokens:
                return False  # Ensure all tokens can be acquired

            rec.count += allowed
        return allowed if not require_all else True

    def try_acquire(self, rate: Rate, key: str, num_tokens: int) -> int:
        return self._try_acquire(rate, key, num_tokens, require_all=False)

    def try_acquire_all(self, rate: Rate, key: str, num_tokens: int) -> bool:
        return self._try_acquire(rate, key, num_tokens, require_all=True)
