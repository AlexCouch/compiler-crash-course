from token_pos import TokenPosition
from token_pos import TokenPositionRange
from lexeme import Lexeme

class SourceFile:
    def __init__(self, source_code, path):
        self.__source_code = source_code
        self.__path = path
        self.__pos = TokenPosition(1, 1, 0)
        self.__curr_char = source_code[self.__pos.pos]

    @property
    def pos(self):
        return self.__pos

    @property
    def source_code(self):
        return self.__source_code

    @property
    def path(self):
        return self.__path

    @property
    def char(self) -> str:
        return self.__curr_char

    def next(self):
        self.next_char()
        return self

    def next_char(self) -> str:
        self.__pos = self.__pos.next()
        if self.__pos.pos not in range(len(self.source_code)):
            self.__curr_char = None
            return None
        self.__curr_char = self.__source_code[self.__pos.pos]
        return self.__curr_char

    def isempty(self) -> bool:
        return self.__curr_char is None

    def new_lexeme(self) -> Lexeme:
        return Lexeme(
            self.char,
            TokenPositionRange(
                self.pos,
                self.pos))

    def new_line(self):
        self.__pos = self.__pos.next_line()
        if self.__pos.pos not in range(len(self.source_code)):
            self.__curr_char = None
            return
        self.__curr_char = self.__source_code[self.__pos.pos]
