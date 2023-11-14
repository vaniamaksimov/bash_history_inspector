import fileinput
import platform
import subprocess
import sys
from pathlib import Path
from types import TracebackType

from app.cli import CliParser
from app.config import Config
from app.lexicon import lexicon
from app.logger import get_logger
from app.models.log import Log
from app.models.log_container import LogContainer
from app.utils.application_types import ApplicationMode, UserOS
from app.utils.errors import InvalidArgumentError, NotSupportedOsError

log = get_logger('application')
config = Config()


class Application:
    def __init__(self) -> None:
        self.cli_parser = CliParser()

    def _check_user_os(self) -> None:
        log.info(lexicon.logger.start_check_user_os)
        user_platform = platform.system()
        log.info(lexicon.logger.user_os(user_platform))
        if not user_platform == UserOS.LINUX:
            raise NotSupportedOsError
        log.info(lexicon.logger.user_os_ok)

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
                raise AssertionError(unreachable)

    def _create_file_if_not_exists(self, filename: str = '.bashrc') -> Path:
        file = Path.home() / filename
        if file.is_file():
            log.info('found file')
        else:
            log.info(f'create {filename} file')
            file.touch(exist_ok=True)
        return file

    def _file_contains_text(self, file: Path | str, text: str) -> bool:
        with open(file) as file_:
            for line in file_:
                if text in line:
                    return True
            return False

    def _replace_line_with_text(
        self, file: Path | str, line: str, text: str = 'HISTTIMEFORMAT="%d/%m/%y %T "'
    ) -> None:
        for line_ in fileinput.input(file, inplace=True):
            if line in line_:
                line_ = line_.replace(line_, text)
            sys.stdout.write(line_)

    def _append_text_to_file(
        self, file: Path | str, text: str = 'HISTTIMEFORMAT="%d/%m/%y %T "'
    ) -> None:
        with open(file, 'a') as file_:
            file_.write('\n')
            file_.write(text)

    def _get_history_logs(self) -> list[str]:
        cmd = subprocess.Popen(
            'bash -i -c \'history -r;history\' ',
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        result, _ = cmd.communicate()
        return list(map(str.strip, result.decode().splitlines()))

    def _convert_raw_logs_to_log_container(self, raw_logs: list[str]) -> LogContainer:
        container = LogContainer()
        for raw_log in raw_logs:
            container.append(Log.from_string(raw_log))
        return container

    def _start_mode(self):
        bashrc = self._create_file_if_not_exists(filename='.bashrc')
        if self._file_contains_text(bashrc, 'HISTTIMEFORMAT'):
            self._replace_line_with_text(bashrc, line='HISTTIMEFORMAT')
        else:
            self._append_text_to_file(bashrc)
        if config.mode == ApplicationMode.HISTORY:
            print('HISTORY')
        else:
            print('CRON')

    def _send_syslog(self, message: str) -> None:
        from syslog import syslog

        syslog(message)

    def start(self):
        self._check_user_os()
        self._read_user_input()
        self._start_mode()

    def __enter__(self):
        log.info(lexicon.logger.start_application)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if not exc_type:
            log.info(lexicon.logger.stop_application_without_error)
            sys.exit(0)
        if isinstance(exc_val, NotSupportedOsError):
            log.error(lexicon.logger.user_os_not_ok)
        elif isinstance(exc_val, InvalidArgumentError):
            log.error(lexicon.logger.invalid_cli_argument)
        # sys.exit(1)
