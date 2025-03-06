from simple_rate_limiter.backends.in_memory import InMemoryBackend
from simple_rate_limiter.rate import Rate
import datetime as dt


def test_empty_state():
    b = InMemoryBackend()

    assert b.try_acquire_all(Rate(10, dt.timedelta(seconds=1)), "", 10)
