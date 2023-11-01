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


class LoggerLexicon(LexiconContainer):
    start_application = {'en_US': 'Starting application', 'ru_RU': 'Инициализируем приложение'}
    start_configurate_arg_parser = {
        'en_US': 'Start configurating argument parser',
        'ru_RU': 'Начинаем инициализацию парсера аргументов',
    }
    start_reading_user_input = {
        'en_US': 'Start reading user input',
        'ru_RU': 'Начинаем чтение пользовательского ввода',
    }
    init_application = {
        'en_US': 'Initialize new application instance',
        'ru_RU': 'Инициализируем новый экземпляр приложения',
    }


class ArgumentParserLexicon(LexiconContainer):
    program_name = {
        'en_US': 'Bash history inspector',
        'ru_RU': 'Инспектор bash истории',
    }
    program_description = {
        'en_US': 'Reading bash history and check for bad commands',
        'ru_RU': 'Читает историю bash команд и ищет команды способные привести в взлому',
    }
    program_epilog = {'en_US': 'CLI arguments:', 'ru_RU': 'Аргументы командной строки'}
    mode_selection = {'en_US': 'Operating mode selection', 'ru_RU': 'Выбор режима работы'}


class Lexicon:
    def __init__(self, user_locale: str) -> None:
        self.argument_parser = ArgumentParserLexicon(user_locale)
        self.logger = LoggerLexicon(user_locale)

    @staticmethod
    def get_lexicon() -> 'Lexicon':
        user_locale, _ = locale.getlocale()
        if not user_locale == 'ru_RU':
            user_locale = 'en_US'
        return Lexicon(user_locale)


lexicon = Lexicon.get_lexicon()
