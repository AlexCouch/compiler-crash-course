from dataclasses import dataclass

@dataclass
class TokenPosition:
    line: int
    col: int
    pos: int

    def next(self):
        return TokenPosition(self.line, self.col + 1, self.pos + 1)

    def next_line(self):
        return TokenPosition(self.line + 1, 1, self.pos + 1)

    def __str__(self):
        return f"{self.line}:{self.col}"

@dataclass
class TokenPositionRange:
    start: TokenPosition
    end: TokenPosition

    def next(self):
        return TokenPositionRange(self.start, self.end.next())

    def reset(self):
        return TokenPositionRange(self.end, self.end)

    def next_line(self):
        return TokenPositionRange(self.end.next_line(), self.end.next_line())

    def __add__(self, other):
        assert isinstance(
            other, TokenPosition), "Expected other to be TokenPosition, not {type(other)}"
        return TokenPositionRange(self.start, other)

    def __str__(self):
        return f"{str(self.start)}-{str(self.end)}"
