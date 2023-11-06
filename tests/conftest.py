from pathlib import Path
from typing import Callable
from uuid import UUID, uuid4

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


@pytest.fixture
def uuid() -> Callable[[], UUID]:
    def fabric() -> UUID:
        return uuid4()

    return fabric


@pytest.fixture
def filename(uuid: Callable[[], UUID]) -> str:
    name = f'test_file_{uuid()}'
    yield name
    (Path.home() / name).unlink(missing_ok=True)


@pytest.fixture
def file_with_text(filename: str) -> tuple[Path, str]:
    dest = Path.home() / filename
    text = 'autotest'
    dest.touch()
    dest.write_text(text)
    return filename, text
