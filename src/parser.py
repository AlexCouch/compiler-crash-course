from tokenstream import TokenStream
from tokens import TokenKind
from astnode import ASTNode
from source_file import SourceFile
from token_pos import TokenPositionRange

from dataclasses import dataclass
from typing import Optional

@dataclass
class ParseResult:
    node: Optional[ASTNode]
    rest: TokenStream
    error_message: 'Optional[tuple[str, TokenPositionRange]]'

    def is_error(self) -> bool:
        return self.error_message is not None

    def is_succ(self) -> bool:
        return self.node is not None

    def is_none(self) -> bool:
        return self.node is None

    @staticmethod
    def some(node, rest) -> 'ParseResult':
        return ParseResult(node, rest, None)

    @staticmethod
    def none(rest) -> 'ParseResult':
        return ParseResult(None, rest, None)

    @staticmethod
    def error(message, pos, rest) -> 'ParseResult':
        return ParseResult(None, rest, (message, pos))

    def to_error(self, message, pos) -> 'ParseResult':
        if self.is_error():
            return self
        return ParseResult.error(message, pos, self.rest) 

    def unwrap(self) -> 'tuple[ASTNode, TokenStream]':
        if not self.is_succ():
            raise "Cannot unwrap None or Error"
        return (self.node, self.rest)

class Parser:
    def parse_ident(self, tokens: TokenStream):
        (ident, rest) = tokens.next()
        if ident.kind.value != TokenKind.IDENT.value and ident.kind.value != TokenKind.WORD.value:  # noqa
            return ParseResult.error(
                f"Expected IDENT or WORD, but instead found {ident.kind.name}", ident.pos, rest)  # noqa
        return ParseResult.some(ASTNode.ident(ident.pos, ident.lexeme), rest)

    def parse_int(self, tokens: TokenStream):
        (token, rest) = tokens.next()
        if token.kind.value != TokenKind.INT.value:
            return ParseResult.error(
                f"Expected integer, but instead got {token.kind.name}",  # noqa
                token.pos,
                rest)
        return ParseResult.some(
            ASTNode.integer(
                token.pos, int(
                    token.lexeme)), rest)

    def parse_refvar(self, tokens: TokenStream):
        (ref, rest) = tokens.next()
        if ref.kind.value != TokenKind.IDENT.value and ref.kind.value != TokenKind.WORD.value:  # noqa
            return ParseResult.none(tokens)
        return ParseResult.some(ASTNode.refvar(ref.lexeme, ref.pos), rest)

    def parse_expression(self, tokens: TokenStream):
        int_result = self.parse_int(tokens)
        if int_result.is_succ():
            return int_result
        ref_result = self.parse_refvar(tokens)
        if ref_result.is_succ():
            return ref_result
        return ParseResult.error("Unrecognized expression", tokens.pos, tokens)

    def parse_varbody(self, var_head: ASTNode, tokens: TokenStream):
        ident = self.parse_ident(tokens)
        if ident.is_error():
            return ident
        # NOTE: We are not checking for none here on ident because it will never # noqa
        # be None
        (ident_node, rest) = ident.unwrap()
        var_head.add_child(ident_node)
        (eq, rest) = rest.next()
        if eq.kind.value != TokenKind.PUNCT.value:
            return ParseResult.error(
                'Expected "="',
                eq.pos, rest
            )
        expr_result = self.parse_expression(rest)
        if expr_result.is_error():
            return expr_result
        (expr, rest) = expr_result.unwrap()
        var_head.add_child(expr)
        return ParseResult.some(var_head, rest)

    def parse_variable(self, tokens: TokenStream):
        var_node = ASTNode.variable(tokens.pos)
        (var, rest) = tokens.next()
        if var.kind.value != TokenKind.WORD.value or var.lexeme != 'var':
            return ParseResult.none(tokens)
        return self.parse_varbody(var_node, rest)

    def parse_const(self, tokens: TokenStream):
        const_node = ASTNode.const(tokens.pos)
        (const, rest) = tokens.next()
        if const.kind.value != TokenKind.WORD.value or const.lexeme != 'const':
            return ParseResult.none(tokens)
        return self.parse_varbody(const_node, rest)

    def parse_varmut(self, tokens: TokenStream):
        mut_node = ASTNode.mut(tokens.pos)
        return self.parse_varbody(mut_node, tokens)

    def parse_statement(self, tokens: TokenStream):
        var_result = self.parse_variable(tokens)
        if var_result.is_succ():
            return var_result
        const_result = self.parse_const(tokens)
        if const_result.is_succ():
            return const_result
        mut_result = self.parse_varmut(tokens)
        if mut_result.is_succ():
            return mut_result

        return ParseResult.error(
            "Unexpected token",
            tokens.next()[0].pos,
            tokens
        )

    def parse(self, source_file: SourceFile, tokens: TokenStream):
        file = ASTNode.file(source_file.path)
        while tokens.notempty():
            statement = self.parse_statement(tokens)
            if statement.is_error():
                return statement
            if statement.is_none():
                return statement
            file.add_child(statement.node)
            tokens = statement.rest
        return ParseResult.some(file, None)
