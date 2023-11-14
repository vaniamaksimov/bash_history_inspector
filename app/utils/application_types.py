from enum import Enum


class ApplicationMode(str, Enum):
    CRON = 'cron'
    HISTORY = 'history'


class UserOS(str, Enum):
    LINUX = 'Linux'
    WINDOWS = 'Windows'
    DARWIN = 'Darwin'
