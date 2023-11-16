from datetime import datetime

import pytest

from app.models.log import Log
from app.models.log_container import LogContainer


@pytest.fixture
def log2025() -> Log:
    return Log(
        1,
        datetime(year=2025, month=1, day=1, hour=1, minute=1, second=1),
        cmd='hello world',
    )


@pytest.fixture
def log2024() -> Log:
    return Log(
        2,
        datetime(year=2024, month=1, day=1, hour=1, minute=1, second=1),
        cmd='hello world',
    )


@pytest.fixture
def log_container(log2025: Log, log2024: Log) -> LogContainer:
    return LogContainer([log2025, log2024])


def test_pop_before_timestamp(log_container: LogContainer, log2025: Log):
    log_container.pop_logs_before_timestamp(
        datetime(year=2024, month=2, day=1, hour=1, minute=1, second=1)
    )
    assert log_container
    assert len(log_container) == 1
    assert log_container[0] == log2025
