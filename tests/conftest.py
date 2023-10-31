from argparse import ArgumentParser

import pytest

from app.config import Config
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
def config() -> Config:
    return Config()


@pytest.fixture
def argument_parser(config: Config) -> ArgumentParser:
    return config.argument_parser
