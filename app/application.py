from types import TracebackType

from config import Config
from lexicon import lexicon
from logger import get_logger

log = get_logger('application')


class Application:
    def __init__(self, config: type[Config]) -> None:
        log.info(lexicon.logger.init_application)
        self.config = config()

    def __check_user_os(self):
        ...

    def __read_user_input(self):
        log.info(lexicon.logger.start_reading_user_input)
        args = self.config.argument_parser.parse_args()
        args

    def start(self):
        self.__check_user_os()
        self.__read_user_input()

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        ...
