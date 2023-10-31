from argparse import ArgumentParser


def test_argument_parser(argument_parser: ArgumentParser):
    args = argument_parser.parse_args(['cron'])
    assert args
