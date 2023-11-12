import re
from dataclasses import dataclass
from datetime import datetime

from app.utils.errors import LogParseError


@dataclass
class Log:
    id: int
    invoke_at: datetime
    cmd: str

    @staticmethod
    def parse_pattern() -> re.Pattern:
        return re.compile(
            r'(?P<number>\d+)\s+(?P<invoke_at>\d{2}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2})\s+(?P<cmd>.+)'
        )

    @classmethod
    def from_string(cls, raw_log: str) -> 'Log':
        match = cls.parse_pattern().match(raw_log)
        if not match:
            raise LogParseError
        log_number = match.group('number')
        log_invoke_at = match.group('invoke_at')
        log_cmd = match.group('cmd')
        return Log(
            id=int(log_number),
            invoke_at=datetime.strptime(log_invoke_at, '%d/%m/%y %H:%M:%S'),
            cmd=log_cmd,
        )
