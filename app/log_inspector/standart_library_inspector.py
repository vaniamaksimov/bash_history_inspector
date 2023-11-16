from app.log_inspector.abc_inspector import AbstractLogInspector
from app.models.log import Log


class StandartLibraryInspector(AbstractLogInspector):
    expertises = [
        ['sudo', 'nc'],
        ['python', '-c', 'import', 'socket'],
        ['python', '-c', 'pty.spawn'],
        ['ncat', '--udp', '-e', '/bin/bash'],
        ['python', '-c', 'eval('],
    ]

    def check_for_dangerous(self, log: Log) -> bool:
        for expertise in self.expertises:
            if all([marker in log.cmd for marker in expertise]):
                return True
        return False
