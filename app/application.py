import fileinput
import platform
import sys
from copy import copy
from datetime import datetime, timedelta
from pathlib import Path
from time import sleep
from types import TracebackType
from typing import TypeVar

from app.cli import CliParser
from app.config import Config
from app.lexicon import lexicon
from app.log_inspector.abc_inspector import AbstractLogInspector
from app.logger import get_logger
from app.models.log import Log
from app.models.log_container import LogContainer
from app.utils.application_types import ApplicationMode, UserOS
from app.utils.errors import InvalidArgumentError, NotSupportedModeError, NotSupportedOsError

logger = get_logger("application")
config = Config()

LogInspectorAdaper = TypeVar("LogInspectorAdaper", bound=AbstractLogInspector)


class Application:
    def __init__(self, log_inspector: LogInspectorAdaper) -> None:
        self.cli_parser = CliParser()
        self.log_inspector = log_inspector

    def _check_user_os(self) -> None:
        logger.info(lexicon.logger.start_check_user_os)
        user_platform = platform.system()
        logger.info(lexicon.logger.user_os(user_platform))
        if not user_platform == UserOS.LINUX:
            raise NotSupportedOsError
        logger.info(lexicon.logger.user_os_ok)

    def _read_user_input(self) -> None:
        logger.info(lexicon.logger.start_reading_user_input)
        namespace = self.cli_parser.parse()
        match namespace.command:
            case ApplicationMode.CRON:
                config.timeout = namespace.minutes
                config.mode = ApplicationMode.CRON
            case ApplicationMode.HISTORY:
                config.mode = ApplicationMode.HISTORY
            case _:
                raise NotSupportedModeError

    def _create_file_if_not_exists(self, filename: str = ".bashrc") -> Path:
        file = Path.home() / filename
        if file.is_file():
            logger.info(lexicon.logger.found_file(filename))
        else:
            logger.info(lexicon.logger.create_file(filename))
            file.touch()
        return file

    def _file_contains_text(self, file: Path | str, text: str) -> bool:
        logger.info(lexicon.logger.start_check_file_for_text(file, text))
        with open(file) as file_:
            for line in file_:
                if text in line:
                    logger.info(lexicon.logger.file_contains_text(file, text))
                    return True
            logger.info(lexicon.logger.file_not_contains_text(file, text))
            return False

    def _replace_line_with_text(
        self, file: Path | str, line: str, text: str = 'HISTTIMEFORMAT="%d/%m/%y %T "'
    ) -> None:
        logger.info(lexicon.logger.start_replace_line_with_text(file, line, text))
        for line_ in fileinput.input(file, inplace=True):
            if line in line_:
                logger.info(lexicon.logger.line_replaced(file, line_, text))
                line_ = line_.replace(line_, text)
            sys.stdout.write(line_)

    def _append_text_to_file(
        self, file: Path | str, text: str = 'HISTTIMEFORMAT="%d/%m/%y %T "'
    ) -> None:
        logger.info(lexicon.logger.append_text_to_file(file, text))
        with open(file, "a") as file_:
            file_.write("\n")
            file_.write(text)

    def _get_history_logs(self, file_name: str = ".bash_history") -> LogContainer:
        logger.info(lexicon.logger.get_logs)
        logs = LogContainer()
        file = Path.home() / file_name
        with open(file, "r") as history_file:
            log_time = None
            for line in history_file:
                if line.startswith("#"):
                    log_time = datetime.fromtimestamp(float(line.removeprefix("#")))
                else:
                    logs.append(
                        Log(
                            invoke_at=log_time if log_time else config.start_time,
                            cmd=line.removesuffix("\n"),
                        )
                    )
                    log_time = None
        return logs

    def _start_history_mode(self) -> None:
        config.start_time = datetime.now()
        logs = self._get_history_logs()
        for log in logs:
            if self.log_inspector.check_for_dangerous(log):
                logger.info(lexicon.logger.find_dangerous_log(log))
                self._send_syslog(log.cmd)

    def _start_cron_mode(self):
        config.start_time = datetime.now()
        config.next_start = config.start_time + timedelta(minutes=config.timeout)
        waiting_message = lexicon.logger.waiting_for_start
        max_i = 3
        while True:
            i = 1
            while datetime.now() < config.next_start:
                sys.stdout.write(f'\r{waiting_message}{"."* i}{" " * (max_i - 1)}')
                sys.stdout.flush()
                sleep(1)
                i += 1
                if i > max_i:
                    i = 1
            sys.stdout.write("\n")
            logs = self._get_history_logs().get_logs_after_timestamp(config.start_time)
            for log in logs:
                if self.log_inspector.check_for_dangerous(log):
                    logger.info(lexicon.logger.find_dangerous_log(log))
                    self._send_syslog(log.cmd)
            config.start_time = copy(config.next_start)
            config.next_start = config.start_time + timedelta(minutes=config.timeout)

    def _start_mode(self) -> None:
        bashrc = self._create_file_if_not_exists(filename=".bashrc")
        if self._file_contains_text(bashrc, "HISTTIMEFORMAT"):
            self._replace_line_with_text(bashrc, line="HISTTIMEFORMAT")
        else:
            self._append_text_to_file(bashrc)
        if config.mode == ApplicationMode.HISTORY:
            self._start_history_mode()
        else:
            self._start_cron_mode()

    def _send_syslog(self, message: str) -> None:
        from syslog import syslog

        syslog(message)

    def start(self):
        self._check_user_os()
        self._read_user_input()
        self._start_mode()

    def __enter__(self) -> "Application":
        logger.info(lexicon.logger.start_application)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if not exc_type:
            logger.info(lexicon.logger.stop_application_without_error)
            sys.exit(0)
        if isinstance(exc_val, NotSupportedOsError):
            logger.error(lexicon.logger.user_os_not_ok)
        elif isinstance(exc_val, InvalidArgumentError):
            logger.error(lexicon.logger.invalid_cli_argument)
        elif isinstance(exc_val, NotSupportedModeError):
            logger.error(lexicon.logger.not_supported_mode_error)
        elif isinstance(exc_val, KeyboardInterrupt):
            logger.info(lexicon.logger.interrupt_by_user)
        sys.exit(1)
