import locale

import pytest
from _pytest.fixtures import SubRequest

from tests.conftest import FakeLexicon


@pytest.mark.parametrize(
    argnames=('locale', 'expected_result'),
    argvalues=(('en_US', 'Bash history inspector'), ('ru_RU', 'Инспектор bash истории')),
)
def test_lexicon_give_text_respect_user_locale(
    locale: str, expected_result: str, fake_lexicon: type[FakeLexicon]
):
    lexicon = fake_lexicon(locale)
    assert lexicon.text.some_text == expected_result


class TestGetLexicon:
    @pytest.fixture
    def locale_(self, request: SubRequest):
        current_locale, _ = locale.getlocale()
        locale.setlocale(locale.LC_ALL, request.param)
        yield request.param
        locale.setlocale(locale.LC_ALL, current_locale)

    @pytest.mark.parametrize('locale_', ('en_US', 'ru_RU'), indirect=True)
    def test_get_lexicon(self, locale_: str, fake_lexicon: type[FakeLexicon]):
        lexicon = fake_lexicon(locale_)
        assert lexicon.text._user_locale == locale_
