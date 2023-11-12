from argparse import ArgumentParser, Namespace

from app.lexicon import lexicon
from app.logger import get_logger

log = get_logger('cli_parser')


class CliParser:
    def __init__(self) -> None:
        self.argument_parser = ArgumentParser()
        self.__post_init__()

    def __post_init__(self):
        self.__configurate_argument_parser()

    def __configurate_argument_parser(self):
        log.info(lexicon.logger.start_configurate_arg_parser)
        self.argument_parser.prog = lexicon.argument_parser.program_name
        self.argument_parser.description = lexicon.argument_parser.program_description
        self.argument_parser.epilog = lexicon.argument_parser.program_epilog
        subparsers = self.argument_parser.add_subparsers(
            dest='command', help=lexicon.argument_parser.mode_selection
        )
        cron_parser = subparsers.add_parser('cron')
        cron_parser.add_argument('-m', '--minutes', dest='minutes', choices=[5, 15, 30], type=int)
        subparsers.add_parser('history')

    def parse(self) -> Namespace:
        return self.argument_parser.parse_args()
