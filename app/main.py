from pathlib import Path

from logger import get_logger

log = get_logger('main')


def main():
    homedir = Path.home()
    log.info('start application')
    with open(homedir / '.bash_history') as bash_history:
        for command in bash_history:
            yield command


if __name__ == '__main__':
    for i in main():
        log.info(f'found command {i}')
        print(i)
