from datetime import datetime

import pytest

from app.models.log import Log


@pytest.fixture
def log_string() -> str:
    return '187 12/11/23 16:02:21 git commit -m "foo"'


def test_log_re_pattern(log_string: str):
    match = Log.parse_pattern().match(log_string)
    assert match
    assert match.group('number')
    assert match.group('number') == '187'
    assert match.group('invoke_at')
    assert match.group('invoke_at') == '12/11/23 16:02:21'
    assert match.group('cmd')
    assert match.group('cmd') == 'git commit -m "foo"'


def test_log_from_string(log_string: str):
    log = Log.from_string(log_string)
    assert log
    assert log.id == 187
    assert log.invoke_at == datetime(year=2023, month=11, day=12, hour=16, minute=2, second=21)
    assert log.cmd == 'git commit -m "foo"'
