import pytest

from lexicon import Lexicon, LexiconContainer


class FakeLexiconContainer(LexiconContainer):
    some_text = {
        'en_US': 'Bash history inspector',
        'ru_RU': 'Испектор bash истории',
    }


class FakeLexicon(Lexicon):
    def __init__(self, user_locale: str) -> None:
        self.text = FakeLexiconContainer(user_locale)


@pytest.fixture
def fake_lexicon() -> type[FakeLexicon]:
    return FakeLexicon
