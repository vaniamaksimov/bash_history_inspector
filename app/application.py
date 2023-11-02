import sys
from syslog import syslog
from types import TracebackType
from typing import assert_never

from cli import CliParser
from lexicon import lexicon
from logger import get_logger

from app.config import Config
from app.utils.application_types import ApplicationMode

log = get_logger('application')
config = Config()


class Application:
    def __init__(self, cli_parser: type[CliParser]) -> None:
        log.info(lexicon.logger.init_application)
        self.cli_parser = cli_parser()

    def _check_user_os(self) -> None:
        if sys.platform == "win32":
            raise

    def _read_user_input(self) -> None:
        log.info(lexicon.logger.start_reading_user_input)
        namespace = self.cli_parser.parse()
        match namespace.command:
            case ApplicationMode.CRON:
                config.timeout = namespace.minutes
                config.mode = ApplicationMode.CRON
            case ApplicationMode.HISTORY:
                config.mode = ApplicationMode.HISTORY
            case _ as unreachable:
                assert_never(unreachable)

    def _start_mode(self):
        ...

    def _send_syslog(self, message: str) -> None:
        syslog(message)

    def start(self):
        self._check_user_os()
        self._read_user_input()
        self._start_mode()

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        ...
