from argparse import ArgumentParser

from lexicon import lexicon
from logger import get_logger
from utils.actions import CronTime

log = get_logger('config')


class Config:
    def __init__(self) -> None:
        self.argument_parser = ArgumentParser()
        self.__post_init__()

    def __post_init__(self):
        self.configurate_argument_parser()

    def configurate_argument_parser(self):
        log.info(lexicon.logger.start_configurate_arg_parser)
        self.argument_parser.prog = lexicon.argument_parser.program_name
        self.argument_parser.description = lexicon.argument_parser.program_description
        self.argument_parser.epilog = lexicon.argument_parser.program_epilog
        subparsers = self.argument_parser.add_subparsers()
        cron_parser = subparsers.add_parser('cron')
        cron_parser.add_argument('--cron', dest='cron', type=CronTime)
        history_parser = subparsers.add_parser('history')
        history_parser.add_argument('--number')
