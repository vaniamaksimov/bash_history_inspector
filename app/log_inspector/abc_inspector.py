from abc import ABC, abstractmethod

from app.models.log import Log


class AbstractLogInspector(ABC):
    @abstractmethod
    def check_for_dangerous(self, log: Log) -> bool:
        ...
