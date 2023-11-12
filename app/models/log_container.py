from collections import UserList

from app.models.log import Log


class LogContainer(UserList[Log]):
    ...
