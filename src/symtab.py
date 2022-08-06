from astnode import ASTNode
from token_pos import TokenPositionRange
from canon import CanonName
from display import Diagnostics

from dataclasses import dataclass
from typing import Optional

@dataclass
class Symbol:
    name: str
    node: ASTNode
    pos: TokenPositionRange

    def dump(self):
        return {
            'name': self.name,
            'node': self.node,
            'pos': self.pos
        }

@dataclass
class Scope:
    name: CanonName
    symbols: list[Symbol]
    children: list['Scope']
    parent: 'Optional[Scope]'

    def find_symbol(self, name):
        for symbol in self.symbols:
            if symbol.name == name:
                return symbol

        for child in self.children:
            sym = child.find_symbol(name)
            if sym:
                return sym
        return None

    def dump(self):
        return {
            'name': self.name,
            'symbols': [symbol.dump() for symbol in self.symbols],
            'children': [child.dump() for child in self.children]
        }

class SymbolTable:
    def __init__(self, diagnostics):
        self.__curr_scope = None
        self.__scopes: list[Scope] = []
        self.__diagnostics = Diagnostics()

    def find_symbol(self, name):
        for scope in self.__scopes:
            sym = scope.find_symbol(name)
            if sym:
                return sym
        return None

    def add_symbol(self, name, node):
        if not self.__curr_scope:
            self.__diagnostics.error(
                    'Attempted to add symbol with no scope, this is a bug in the compile',  # noqa
                    node.pos)
            return False
        canonName = CanonName(
            name, self.__curr_scope.name if self.__curr_scope else None)
        self.__curr_scope.symbols.append(
            Symbol(canonName,
                   node,
                   node.pos))

    def enter_scope(self, node):
        for child in self.__curr_scope.children:
            if child.name == node.name:
                self.curr_scope = child
                return

        if not self.__curr_scope:
            self.__curr_scope = Scope(
                CanonName(node.name, None),
                [], [], None)
            return
        canonName = CanonName(node.name, self.__curr_scope.name)
        scope = Scope(canonName, [], [], self.__curr_scope)
        self.__curr_scope.children.append(scope)
        self.__curr_scope = scope

    def exit_scope(self):
        if self.__curr_scope and self.__curr_scope.parent:
            self.__curr_scope = self.__curr_scope.parent

    def dump(self):
        scope = self.__curr_scope
        return scope.dump()
