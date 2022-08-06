from tokens import Token

class TokenStream:
    def __init__(self, tokens):
        self.__pos = tokens[0].pos if len(tokens) > 0 else None
        self.__tokens = tokens

    @property
    def pos(self):
        return self.__pos

    def next(self) -> 'tuple[Token, TokenStream]':
        token = self.__tokens[0]
        new = TokenStream(self.__tokens[1:])
        return (token, new)

    def notempty(self):
        return len(self.__tokens) > 0
