from collections import UserList
from datetime import datetime

from app.models.log import Log


class LogContainer(UserList[Log]):
    def get_logs_after_timestamp(self, timestamp: datetime) -> 'LogContainer':
        logs = LogContainer()
        for log in self:
            if log.invoke_at > timestamp:
                logs.append(log)
        return logs
