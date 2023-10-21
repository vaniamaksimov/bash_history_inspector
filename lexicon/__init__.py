import platform
from dataclasses import dataclass


@dataclass
class ArgumentParserLexicon:
    program_name = {
        'en_US': 'Bash history inspector',
        'ru_RU': 'Испектор bash истории',
    }


class Lexicon:
    def __init__(self, user_language: str) -> None:
        self.user_language = user_language


if platform.system() in ('Linux', 'Darwin'):
    import os

    user_language = os.getenv('LANG').split('.')[0]
    lexicon = ...
else:
    import ctypes
    import locale

    user_language = locale.windows_locale[ctypes.windll.GetUserDefaultUILanguage()]
    lexicon = ...

lexicon = Lexicon()
