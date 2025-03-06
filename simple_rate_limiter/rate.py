import datetime as dt
from dataclasses import dataclass


@dataclass
class Rate:
    max_tokens: int
    period: dt.timedelta
