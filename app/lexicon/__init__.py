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
    start_reading_user_input = {
        'en_US': 'Start reading user input',
        'ru_RU': 'Начинаем чтение пользовательского ввода',
    }
    start_check_user_os = {
        'en_US': 'Start checking user os',
        'ru_RU': 'Проверяем пользовательскую операционную систему',
    }
    init_application = {
        'en_US': 'Initialize new application instance',
        'ru_RU': 'Инициализируем новый экземпляр приложения',
    }
    user_os = {
        'en_US': lambda os: f'User os is {os}',
        'ru_RU': lambda os: f'Операционная система пользователя {os}',
    }
    user_os_ok = {
        'en_US': 'User os accepted',
        'ru_RU': 'Пользовательская операционная система принята',
    }
    stop_application_without_error = {
        'en_US': 'Stop application without errors',
        'ru_RU': 'Останавливаем приложение без внутренних ошибок',
    }
    user_os_not_ok = {
        'en_US': 'Not supported user os',
        'ru_RU': 'Пользовательская операционная система не поддерживается',
    }
    invalid_cli_argument = {
        'en_US': 'Invalid cli argument',
        'ru_RU': 'Передан неверный аргумент командной строки',
    }
    succesfull_read_user_input = {
        'en_US': 'Succesfull read user input',
        'ru_RU': 'Пользовательский ввод успешно прочитан',
    }
    not_supported_mode_error = {
        'en_US': 'Not supported operating mode',
        'ru_RU': 'Выбранный режим не поддерживается',
    }
    found_file = {
        'en_US': lambda filename: f'File {filename} founded',
        'ru_RU': lambda filename: f'Файл {filename} найден',
    }
    create_file = {
        'en_US': lambda filename: f'Creating file {filename}',
        'ru_RU': lambda filename: f'Создаём файл {filename}',
    }
    start_check_file_for_text = {
        'en_US': lambda file, text: f'Start checking file {file} for text {text}',
        'ru_RU': lambda file, text: f'Начинаем поиск в файле {file} текста {text}',
    }
    file_contains_text = {
        'en_US': lambda file, text: f'File {file} contains text {text}',
        'ru_RU': lambda file, text: f'Файл {file} содержит текст {text}',
    }
    file_not_contains_text = {
        'en_US': lambda file, text: f'File {file} dont contains text {text}',
        'ru_RU': lambda file, text: f'Файл {file} не содержит текст {text}',
    }
    start_replace_line_with_text = {
        'en_US': lambda file, line, text: (
            f'Start replace in file {file} line with text {line} for text {text}'
        ),
        'ru_RU': lambda file, line, text: (
            f'Начинаем заменять в файле {file} строку с текстом {line} на текст {text}'
        ),
    }
    line_replaced = {
        'en_US': lambda file, line, text: f'Replace in file {file} line {line} for {text}',
        'ru_RU': lambda file, line, text: f'Заменяем в файле {file} строку {line} на строку {text}',
    }
    append_text_to_file = {
        'en_US': lambda file, text: f'Appendind text {text} to file {file}',
        'ru_RU': lambda file, text: f'Добавляем текст {text} в файл {file}',
    }


class ArgumentParserLexicon(LexiconContainer):
    program_name = {
        'en_US': 'python history_inspector.py',
        'ru_RU': 'python history_inspector.py',
    }
    program_description = {
        'en_US': 'Reading bash history and check for bad commands',
        'ru_RU': 'Читает историю bash команд и ищет команды способные привести в взлому',
    }
    mode_selection = {'en_US': 'Operating mode selection', 'ru_RU': 'Выбор режима работы'}
    cron_help = {'en_US': 'Cron time selection in minutes', 'ru_RU': 'Выбор времени cron в минутах'}


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
