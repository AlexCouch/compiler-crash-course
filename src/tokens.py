from enum import Enum
from token_pos import TokenPositionRange
from dataclasses import dataclass

class TokenKind(Enum):
    WORD = 0
    IDENT = 1
    INT = 2
    FLOAT = 3
    PUNCT = 4

@dataclass
class Token:
    lexeme: str
    pos: TokenPositionRange
    file: str
    kind: TokenKind

    def __str__(self):
        return f'{self.kind}-{self.lexeme}@{self.file}:{self.pos}'
