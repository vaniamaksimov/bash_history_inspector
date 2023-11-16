from collections import UserList
from datetime import datetime

from app.models.log import Log


class LogContainer(UserList[Log]):
    def pop_logs_before_timestamp(self, timestamp: datetime) -> 'LogContainer':
        for index, log in enumerate(self):
            if log.invoke_at < timestamp:
                self.pop(index)
        return self
