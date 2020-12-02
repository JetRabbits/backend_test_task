import datetime
import random

from datetime import timezone

MIN_MINUTES = 29
MAX_MINUTES = 59

MIN_START_HOURS = 3
MAX_START_HOURS = 9

MIN_END_HOURS = 20
MAX_END_HOURS = 23


def start_date():
    t = datetime.time(hour=random.randint(MIN_START_HOURS, MAX_START_HOURS),
                      minute=random.randint(MIN_MINUTES, MAX_MINUTES))
    return datetime.datetime.combine(datetime.datetime.now(timezone.utc), t, timezone.utc)


def end_date():
    t = datetime.time(hour=random.randint(MIN_END_HOURS, MAX_END_HOURS), minute=59)
    return datetime.datetime.combine(datetime.datetime.now(timezone.utc), t, timezone.utc)