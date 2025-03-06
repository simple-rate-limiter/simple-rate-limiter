import datetime as dt
from dataclasses import dataclass

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
