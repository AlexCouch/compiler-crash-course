from symtab import SymbolTable
from astnode import ASTNode
from token_pos import TokenPositionRange, TokenPosition

import pprint

varnode = ASTNode.variable(TokenPositionRange(
    TokenPosition(1, 1, 0), TokenPosition(1, 1, 0)
))
ident = ASTNode.ident(
    TokenPositionRange(
        TokenPosition(
            1, 1, 0), 
        TokenPosition(
            1, 1, 0)), 
    'test')
varnode.add_child(ident)
root = ASTNode.file('test.ag')
symtable = SymbolTable(root)
symtable.enter_scope(root)
symtable.add_symbol(ident.data, varnode)
symtable.exit_scope()

pretty_printer = pprint.PrettyPrinter(indent=4)
test_find_symbol = symtable.find_symbol('test')
pretty_printer.pprint(test_find_symbol.dump())

table_dump = symtable.dump()
pretty_printer.pprint(table_dump)
