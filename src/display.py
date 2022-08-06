from enum import Enum
from token_pos import TokenPositionRange
from source_file import SourceFile

class DiagnosticLevel(Enum):
    ERROR = 0
    WARNING = 1
    INFO = 2

class DiagnosticColor(Enum):
    RED = 91
    YELLOW = 93
    BLUE = 94
    RESET = 0

    def get_ansi(self):
        return f'\033[{self.value}m'

class Diagnostics:
    def __init__(self, source_file):
        self.__source_file: SourceFile = source_file

    def display(
            self,
            level: DiagnosticLevel,
            message: str,
            pos: TokenPositionRange):

        prefix = level.name
        if level == DiagnosticLevel.ERROR:
            color = DiagnosticColor.RED.get_ansi()
        elif level == DiagnosticLevel.WARNING:
            color = DiagnosticColor.YELLOW.get_ansi()
        elif level == DiagnosticLevel.INFO:
            color = DiagnosticColor.BLUE.get_ansi()
        lines = self.__source_file.source_code.splitlines()
        line = lines[pos.start.line - 1]
        before = line[0:pos.start.col - 1]
        after = line[pos.end.col:]
        offender = line[pos.start.col - 1:pos.end.col]
        print(
            f'{color}[{prefix}] - {self.__source_file.path} @ {pos} - {message}{DiagnosticColor.RESET.get_ansi()}')  # noqa
        print(
            f'    {before}{color}{offender}{DiagnosticColor.RESET.get_ansi()}{after}')

    def error(self, message, pos):
        self.display(DiagnosticLevel.ERROR, message, pos)

    def warning(self, message, pos):
        self.display(DiagnosticLevel.WARNING, message, pos)

    def info(self, message, pos):
        self.display(DiagnosticLevel.INFO, message, pos)

