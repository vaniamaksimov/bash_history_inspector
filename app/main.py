from application import Application
from config import Config
from lexicon import lexicon
from logger import get_logger

log = get_logger('main')


if __name__ == '__main__':
    log.info(lexicon.logger.start_application)
    with Application(config=Config) as app:
        app.start()
