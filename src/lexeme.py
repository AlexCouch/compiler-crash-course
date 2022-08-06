from dataclasses import dataclass
from token_pos import TokenPosition, TokenPositionRange

@dataclass
class Lexeme:
    buffer: str
    pos: TokenPositionRange

    def add(self, char: str, pos: TokenPosition):
        return Lexeme(self.buffer + char, self.pos + pos)
