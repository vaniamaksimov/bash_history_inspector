from app.application import Application
from app.cli import CliParser

app = Application(CliParser)
bashrc = app._create_file_if_not_exists()
if app._file_contains_text(bashrc, 'HISTTIMEFORMAT'):
    app._replace_line_with_text(bashrc, 'HISTTIMEFORMAT')
else:
    app._append_text_to_file(bashrc)

print(app._get_history_logs())
