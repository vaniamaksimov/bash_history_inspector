import logging
import logging.config
import sys

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'root': {
            'level': 'INFO',
            'handlers': ['default'],
        },
        'main': {
            'level': 'INFO',
            'handlers': ['default'],
            'propagate': False,
        },
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'standard',
        },
        'error': {'class': 'logging.StreamHandler', 'stream': sys.stderr, 'formatter': 'standard'},
    },
    'formatters': {'standard': {'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'}},
}
logging.config.dictConfig(logging_config)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
