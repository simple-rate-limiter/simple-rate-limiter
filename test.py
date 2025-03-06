from simple_rate_limiter.backends.in_memory import InMemoryBackend
from simple_rate_limiter.rate_limiter import RateLimiter

rl = RateLimiter(
    max_tokens=3,
    period=1,
    backend=InMemoryBackend()
)

DATA = [8] * 10


def process1(request, value):
    if rl.try_acquire_all(key=request.ip):
        return value + 10
    else:
        raise


def process2(request, value):
    if rl.try_acquire_all(key=request.ip, num_tokens=value):
        return DATA
    else:
        raise


def process3(request, value):
    if allowed := rl.try_acquire(key=request.ip, num_tokens=value):
        return DATA[:allowed]
    else:
        raise
