from pathlib import Path

from logger import get_logger

log = get_logger('main')


def main():
    homedir = Path.home()
    # os.environ['HISTTIMEFORMAT'] = '%F %T '
    log.info('start application')
    file = Path(homedir / '.bashrc')
    if file.exists() and file.is_file():
        log.info('file exists')
    else:
        log.info('file not exists')
    # with open(homedir / '.bashrc') as file:
    #     print(file)
    # with open(homedir / '.bash_history') as bash_history:
    #     for command in bash_history:
    #         yield command


if __name__ == '__main__':
    main()
    # for i in range(readline.read_history_file('~/.bash_history')):
    # for i in main():
    #     # log.info(f'found command {i}')
    #     print(i)
