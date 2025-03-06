from freezegun import freeze_time

from simple_rate_limiter.rate import Rate
import datetime as dt


def test_empty_state_partial(backend):
    rate = Rate(10, dt.timedelta(seconds=1))

    assert backend.try_acquire_all(rate, "1", 5)


def test_empty_state_full(backend):
    rate = Rate(10, dt.timedelta(seconds=1))

    assert backend.try_acquire_all(rate, "1", 10)


def test_empty_state_full_multiple_tries(backend):
    rate = Rate(10, dt.timedelta(seconds=1))

    assert backend.try_acquire_all(rate, "1", 3)
    assert backend.try_acquire_all(rate, "1", 7)


def test_empty_state_full_multiple_keys(backend):
    rate = Rate(10, dt.timedelta(seconds=1))

    assert backend.try_acquire_all(rate, "1", 3)
    assert backend.try_acquire_all(rate, "1", 7)

    assert backend.try_acquire_all(rate, "2", 3)
    assert backend.try_acquire_all(rate, "2", 7)


def test_single_key_overflow(backend):
    rate = Rate(10, dt.timedelta(seconds=10))

    start = dt.datetime(2025, 1, 1, 0, 0, 0)

    with freeze_time(start):
        assert backend.try_acquire_all(rate, "1", 10)

    with freeze_time(start + dt.timedelta(seconds=3)):
        assert not backend.try_acquire_all(rate, "1", 1)

    with freeze_time(start + dt.timedelta(seconds=11)):
        assert not backend.try_acquire_all(rate, "1", 5)
        assert backend.try_acquire_all(rate, "1", 1)


def test_multiple_keys_overflow(backend):
    rate = Rate(10, dt.timedelta(seconds=10))

    start = dt.datetime(2025, 1, 1, 0, 0, 0)

    with freeze_time(start):
        assert backend.try_acquire_all(rate, "1", 10)

    with freeze_time(start + dt.timedelta(seconds=1)):
        assert backend.try_acquire_all(rate, "2", 10)

    with freeze_time(start + dt.timedelta(seconds=11)):
        assert not backend.try_acquire_all(rate, "1", 5)
        assert backend.try_acquire_all(rate, "1", 1)

    with freeze_time(start + dt.timedelta(seconds=11)):
        assert not backend.try_acquire_all(rate, "2", 5)
        assert not backend.try_acquire_all(rate, "2", 1)


def test_two_full_windows_passed(backend):
    rate = Rate(10, dt.timedelta(seconds=10))

    start = dt.datetime(2025, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc)

    with freeze_time(start):
        assert backend.try_acquire_all(rate, "1", 10)

    with freeze_time(start + dt.timedelta(seconds=33)):
        assert backend.try_acquire_all(rate, "1", 10)

    with freeze_time(start + dt.timedelta(seconds=34)):
        assert not backend.try_acquire_all(rate, "1", 1)
