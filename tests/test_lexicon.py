import platform

import pytest

from lexicon import Lexicon


@pytest.mark.parametrize(
    argnames=('locale', 'expected_result'),
    argvalues=(('en_US', 'Bash history inspector'), ('ru_RU', 'Испектор bash истории')),
)
def test_lexicon_give_text_respect_user_locale(locale: str, expected_result: str):
    lexicon = Lexicon(locale)
    assert lexicon.argument_parser.program_name == expected_result


@pytest.mark.skipif(
    lambda _: platform.system() not in ('Linux', 'Darwin'), reason='dont work on Windows'
)
class TestGetLexicon:
    def test_get_lexicon(self):
        ...
