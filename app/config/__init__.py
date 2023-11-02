from app.utils.singleton import SingletonMeta


class Config(metaclass=SingletonMeta):
    def __init__(self, timeout: int | None = None, mode: str | None = None) -> None:
        self.timeout = timeout
        self.mode = mode
