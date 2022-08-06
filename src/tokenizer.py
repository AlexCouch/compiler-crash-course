from dataclasses import dataclass
from enum import Enum
from source_file import SourceFile
from token_pos import TokenPositionRange

from string import punctuation

PUNCTS = set(punctuation)

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


class Tokenizer:
    def tokenize(self, source_code: SourceFile) -> list[Token]:
        tokens = []
        while not source_code.isempty():
            char: str = source_code.char
            if char.isdigit():
                lexeme = source_code.new_lexeme()
                while source_code.char.isdigit():
                    source_code = source_code.next()
                    if not source_code.char.isdigit():
                        break
                    lexeme = lexeme.add(source_code.char, source_code.pos)
                    if source_code.char == '.':
                        source_code = source_code.next()
                        lexeme = lexeme.add(source_code.char, source_code.pos)
                        continue

                tokens.append(
                    Token(
                        lexeme.buffer,
                        lexeme.pos,
                        source_code.path,
                        TokenKind.INT if lexeme.buffer.isdigit() else TokenKind.FLOAT))  # noqa
                # source_code = source_code.next()
            elif char.isalpha():
                lexeme = source_code.new_lexeme()
                while source_code.char.isalnum():
                    source_code = source_code.next()
                    if not source_code.char.isalnum():
                        break
                    lexeme = lexeme.add(source_code.char, source_code.pos)
                tokens.append(
                    Token(
                        lexeme.buffer,
                        lexeme.pos,
                        source_code.path,
                        TokenKind.WORD if lexeme.buffer.isalpha() else TokenKind.IDENT))  # noqa
                # source_code = source_code.next()
            elif char in PUNCTS:
                lexeme = source_code.new_lexeme()
                tokens.append(
                    Token(
                        lexeme.buffer,
                        lexeme.pos,
                        source_code.path,
                        TokenKind.PUNCT))
                source_code = source_code.next()
            elif char == '\n':
                source_code.new_line()
            elif char.isspace():
                source_code = source_code.next()

        return tokens
