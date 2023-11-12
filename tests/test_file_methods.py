from pathlib import Path

import pytest

from app.application import Application


def test_creating_file_if_not_exists(application: Application, filename: str):
    file = application._create_file_if_not_exists(filename=filename)
    assert file.is_file()


def test_creating_file_if_exists_dont_rewrite_text(
    application: Application, file_with_text: tuple[Path, str]
):
    filename, text = file_with_text
    file = application._create_file_if_not_exists(filename=filename)
    file_text = file.read_text()
    assert file_text == text


@pytest.mark.parametrize(
    argnames=['text', 'expected_result'],
    argvalues=[
        ['autotest', True],
        ['Autotest', False],
        ['aautotest', False],
    ],
)
def test_file_contains_text_method(
    application: Application, file_with_text: tuple[Path, str], text: str, expected_result: bool
):
    file, _ = file_with_text
    result = application._file_contains_text((Path.home() / file), text)
    assert result == expected_result


def test_replace_line_with_text_method(application: Application, file_with_text: tuple[Path, str]):
    file_name, text = file_with_text
    dest = Path.home() / file_name
    application._replace_line_with_text(dest, text)
    file_text = dest.read_text()
    assert file_text == 'HISTTIMEFORMAT="%d/%m/%y %T "'


def test_apend_text_to_file(application: Application, file_with_text: tuple[Path, str]):
    file_name, text = file_with_text
    dest = Path.home() / file_name
    application._append_text_to_file(dest)
    file_text = dest.read_text()
    assert file_text == f'{text}\nHISTTIMEFORMAT="%d/%m/%y %T "'
