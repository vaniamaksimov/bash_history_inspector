from enum import Enum


class ApplicationMode(str, Enum):
    CRON = 'cron'
    HISTORY = 'history'
