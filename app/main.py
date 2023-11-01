from application import Application
from cli import CliParser
from lexicon import lexicon
from logger import get_logger

log = get_logger('main')


if __name__ == '__main__':
    log.info(lexicon.logger.start_application)
    with Application(cli_parser=CliParser) as app:
        app.start()
