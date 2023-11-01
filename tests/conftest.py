import pytest

from app.application import Application
from app.cli import CliParser
from app.lexicon import Lexicon, LexiconContainer


class FakeLexiconContainer(LexiconContainer):
    some_text = {
        'en_US': 'Bash history inspector',
        'ru_RU': 'Инспектор bash истории',
    }


class FakeLexicon(Lexicon):
    def __init__(self, user_locale: str) -> None:
        self.text = FakeLexiconContainer(user_locale)


@pytest.fixture
def fake_lexicon() -> type[FakeLexicon]:
    return FakeLexicon


@pytest.fixture
def application() -> Application:
    return Application(cli_parser=CliParser)


@pytest.fixture
def argument_parser(application: Application) -> CliParser:
    return application.cli_parser
