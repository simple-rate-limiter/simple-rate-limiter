from freezegun import freeze_time

from simple_rate_limiter.backends.in_memory import InMemoryBackend
from simple_rate_limiter.rate import Rate
import datetime as dt


def test_empty_state_partial():
    b = InMemoryBackend()

    rate = Rate(10, dt.timedelta(seconds=1))

    assert b.try_acquire_all(rate, "1", 5)


def test_empty_state_full():
    b = InMemoryBackend()

    rate = Rate(10, dt.timedelta(seconds=1))

    assert b.try_acquire_all(rate, "1", 10)


def test_empty_state_full_multiple_tries():
    b = InMemoryBackend()

    rate = Rate(10, dt.timedelta(seconds=1))

    assert b.try_acquire_all(rate, "1", 3)
    assert b.try_acquire_all(rate, "1", 7)


def test_empty_state_full_multiple_keys():
    b = InMemoryBackend()

    rate = Rate(10, dt.timedelta(seconds=1))

    assert b.try_acquire_all(rate, "1", 3)
    assert b.try_acquire_all(rate, "1", 7)

    assert b.try_acquire_all(rate, "2", 3)
    assert b.try_acquire_all(rate, "2", 7)


def test_single_key_overflow():
    b = InMemoryBackend()

    rate = Rate(10, dt.timedelta(seconds=10))

    start = dt.datetime(2025, 1, 1, 0, 0, 0)

    with freeze_time(start):
        assert b.try_acquire_all(rate, "1", 10)

    with freeze_time(start + dt.timedelta(seconds=3)):
        assert not b.try_acquire_all(rate, "1", 1)

    with freeze_time(start + dt.timedelta(seconds=11)):
        assert not b.try_acquire_all(rate, "1", 5)
        assert b.try_acquire_all(rate, "1", 1)


def test_multiple_keys_overflow():
    b = InMemoryBackend()

    rate = Rate(10, dt.timedelta(seconds=10))

    start = dt.datetime(2025, 1, 1, 0, 0, 0)

    with freeze_time(start):
        assert b.try_acquire_all(rate, "1", 10)

    with freeze_time(start + dt.timedelta(seconds=1)):
        assert b.try_acquire_all(rate, "2", 10)

    with freeze_time(start + dt.timedelta(seconds=11)):
        assert not b.try_acquire_all(rate, "1", 5)
        assert b.try_acquire_all(rate, "1", 1)

    with freeze_time(start + dt.timedelta(seconds=11)):
        assert not b.try_acquire_all(rate, "2", 5)
        assert not b.try_acquire_all(rate, "2", 1)


def test_two_full_windows_passed():
    b = InMemoryBackend()

    rate = Rate(10, dt.timedelta(seconds=10))

    start = dt.datetime(2025, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc)

    with freeze_time(start):
        assert b.try_acquire_all(rate, "1", 10)

    with freeze_time(start + dt.timedelta(seconds=33)):
        assert b.try_acquire_all(rate, "1", 10)

    assert b._storage["1"].window_start == start + dt.timedelta(seconds=33)

    with freeze_time(start + dt.timedelta(seconds=34)):
        assert not b.try_acquire_all(rate, "1", 1)
