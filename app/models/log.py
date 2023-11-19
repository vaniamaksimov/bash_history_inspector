from dataclasses import dataclass
from datetime import datetime


@dataclass
class Log:
    invoke_at: datetime
    cmd: str
