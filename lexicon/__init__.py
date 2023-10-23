import locale
from typing import Any


class ArgumentParserLexicon:
    program_name = {
        'en_US': 'Bash history inspector',
        'ru_RU': 'Испектор bash истории',
    }

    def __init__(self, user_language: str) -> None:
        self.__user_locale = user_language

    def __getattribute__(self, __name: str) -> Any:
        attr = object.__getattribute__(self, __name)
        if isinstance(attr, dict) and not __name.startswith('_'):
            return attr[self.__user_locale]
        return attr


class Lexicon:
    def __init__(self, user_locale: str) -> None:
        self.argument_parser = ArgumentParserLexicon(user_locale)


def get_lexicon() -> Lexicon:
    user_locale, _ = locale.getlocale()
    if not user_locale == 'ru_RU':
        user_locale = 'en_US'
    return Lexicon(user_locale)
