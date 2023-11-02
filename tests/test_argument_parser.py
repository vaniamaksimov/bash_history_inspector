import pytest

from app.cli import CliParser


@pytest.mark.parametrize(
    argnames=['command', 'expected'], argvalues=[[['cron'], 'cron'], [['history'], 'history']]
)
def test_argument_parser(argument_parser: CliParser, command: list[str], expected: str):
    namespace = argument_parser.argument_parser.parse_args(command)
    assert namespace.command == expected


def test_cron_parser(argument_parser: CliParser):
    namespace = argument_parser.argument_parser.parse_args(['cron', '-m', '5'])
    assert namespace.command == 'cron'
    assert namespace.minutes == 5
