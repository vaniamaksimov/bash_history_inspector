import locale
from abc import ABC
from typing import Any


class LexiconContainer(ABC):
    def __init__(self, user_language: str) -> None:
        self._user_locale = user_language

    def __getattribute__(self, __name: str) -> Any:
        attr = object.__getattribute__(self, __name)
        if isinstance(attr, dict) and not __name.startswith('_'):
            return attr[self._user_locale]
        return attr


class ArgumentParserLexicon(LexiconContainer):
    program_name = {
        'en_US': 'Bash history inspector',
        'ru_RU': 'Испектор bash истории',
    }


class Lexicon:
    def __init__(self, user_locale: str) -> None:
        self.argument_parser = ArgumentParserLexicon(user_locale)

    @classmethod
    def get_lexicon() -> 'Lexicon':
        user_locale, _ = locale.getlocale()
        if not user_locale == 'ru_RU':
            user_locale = 'en_US'
        return Lexicon(user_locale)
