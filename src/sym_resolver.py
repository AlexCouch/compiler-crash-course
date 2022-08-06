from visitor import Visitor
from display import Diagnostics
from symtab import SymbolTable
from astnode import ASTNode

class SymbolResolver:
    def __init__(self, diagnostics, source_file):
        self.__diagnostics: Diagnostics = diagnostics
        self.__symbol_table = SymbolTable(self.__diagnostics)
        self.__visitor = Visitor()

        self.__visitor.add_visitor('const', self.visitVar)
        self.__visitor.add_visitor('var', self.visitVar)
        self.__visitor.add_visitor('refvar', self.visitRefVar)
        self.__visitor.add_visitor('mut', self.visitMut)


    @property
    def visitor(self):
        return self.__visitor

    @property
    def symbol_table(self):
        return self.__symbol_table

    def enter_file(self, path):
        self.__symbol_table.enter_scope(ASTNode.file(path))

    def visitVar(self, node):
        ident = node.children[0]
        if not self.__symbol_table.find_symbol(ident.data):
            if self.__symbol_table.add_symbol(ident.data, ident) is False:
                return False

    def visitMut(self, node):
        ident = node.children[0]
        if not self.__symbol_table.find_symbol(ident.data):
            self.__diagnostics.error('Could not find symbol', ident.pos)
            return False

    def visitRefVar(self, node):
        if not self.__symbol_table.find_symbol(node.data):
            self.__diagnostics.error('Could not find symbol', node.pos)
            return False
