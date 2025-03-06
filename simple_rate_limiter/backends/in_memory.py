import datetime as dt
import threading
from dataclasses import dataclass
from collections import defaultdict

from simple_rate_limiter.backends._base import BaseBackend
from simple_rate_limiter.rate import Rate


@dataclass
class Record:
    window_start: dt.datetime
    prev_count: int = 0
    count: int = 0

    def calculate_current_rate(self, rate: Rate, now: dt.datetime) -> float:
        return (
            self.prev_count * (1 - (now - self.window_start).total_seconds() / rate.period.total_seconds()) + self.count
        )

    def sync(self, rate: Rate, now: dt.datetime) -> None:
        period_since_window_start = now - self.window_start
        if period_since_window_start >= rate.period:
            if period_since_window_start >= 2 * rate.period:
                self.window_start = now
                self.prev_count = 0
                self.count = 0
            else:
                self.window_start += rate.period
                self.prev_count = self.count
                self.count = 0


class InMemoryBackend(BaseBackend):
    def __init__(self):
        self.storage: dict[str, Record] = {}
        self._locks: dict[str, threading.Lock] = defaultdict(threading.Lock)

    def try_acquire(self, rate: Rate, key: str, num_tokens: int) -> int:
        with self._locks[key]:
            now = dt.datetime.now(dt.UTC)
            rec = self.storage.setdefault(key, Record(now, 0, 0))
            rec.sync(rate, now)
            allowed = max(
                min(rate.max_tokens - rec.calculate_current_rate(rate, now), num_tokens),
                0,
            )
            rec.count += allowed
        return allowed

    def try_acquire_all(self, rate: Rate, key: str, num_tokens: int) -> bool:
        with self._locks[key]:
            now = dt.datetime.now(dt.UTC)
            rec = self.storage.setdefault(key, Record(now, 0, 0))
            rec.sync(rate, now)
            if rate.max_tokens - rec.calculate_current_rate(rate, now) - num_tokens < 0:
                return False
            rec.count += num_tokens
        return True
