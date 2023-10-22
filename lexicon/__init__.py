import platform
from typing import Any


class ArgumentParserLexicon:
    program_name = {
        'en_US': 'Bash history inspector',
        'ru_RU': 'Испектор bash истории',
    }

    def __init__(self, user_language: str) -> None:
        self.__user_language = user_language

    def __getattribute__(self, __name: str) -> Any:
        attr = object.__getattribute__(self, __name)
        if isinstance(attr, dict) and not __name.startswith('_'):
            return attr[self.__user_language]
        return attr


class Lexicon:
    def __init__(self, user_language: str) -> None:
        self.argument_parser = ArgumentParserLexicon(user_language)


def get_lexicon() -> Lexicon:
    if platform.system() in ('Linux', 'Darwin'):
        import os

        user_language = os.getenv('LANG').split('.')[0]
    else:
        import ctypes
        import locale

        windll = ctypes.windll.kernel32
        user_language = locale.windows_locale[windll.GetUserDefaultUILanguage()]

    return Lexicon(user_language)
