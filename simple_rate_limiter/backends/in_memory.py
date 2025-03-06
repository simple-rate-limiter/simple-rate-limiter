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

    def try_acquire(self, rate: Rate, key: str, num_tokens: int) -> int:
        with self._locks[key]:
            now = dt.datetime.now(dt.UTC)
            rec = self._storage.setdefault(key, Record(now, 0, 0))
            allowed = self.get_allowed(now, num_tokens, rate, rec)
            rec.count += allowed
        return allowed

    def try_acquire_all(self, rate: Rate, key: str, num_tokens: int) -> bool:
        with self._locks[key]:
            now = dt.datetime.now(dt.UTC)
            rec = self._storage.setdefault(key, Record(now, 0, 0))
            rec.sync(rate, now)
            allowed = self.get_allowed(now, num_tokens, rate, rec)
            if allowed != num_tokens:
                return False
            rec.count += num_tokens
        return True
