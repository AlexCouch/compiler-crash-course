from visitor import Visitor

class DebugPrinter:
    def __init__(self):
        self.__buffer = ""
        self.__indent = 0

    def append(self, appendee):
        self.__buffer += '    ' * self.__indent
        self.__buffer += appendee

    def newline(self):
        self.__buffer += '\n'

    def enter(self):
        self.__indent += 1

    def exit(self):
        self.__indent -= 1

    def dump(self):
        return self.__buffer

    def reset(self):
        self.__buffer = ''

class ASTPrinter:
    def __init__(self):
        self.__visitor = Visitor()
        self.__visitor.add_visitor('file', self.visitFile)
        self.__visitor.add_visitor('const', self.visitConst)
        self.__visitor.add_visitor('var', self.visitVar)
        self.__visitor.add_visitor('ident', self.visitIdent)
        self.__visitor.add_visitor('int', self.visitInt)

        self.__visitor.add_leaver('file', self.leaveFile)
        self.__visitor.add_leaver('const', self.leaveConst)
        self.__visitor.add_leaver('var', self.leaveVar)

        self.__debug_printer = DebugPrinter()

    @property
    def visitor(self):
        return self.__visitor

    @property
    def printer(self):
        return self.__debug_printer

    def visitFile(self, node):
        self.__debug_printer.append("File: " + node.data)
        self.__debug_printer.newline()
        self.__debug_printer.enter()

    def leaveFile(self, node):
        self.__debug_printer.exit()

    def visitConst(self, node):
        self.__debug_printer.append("Const:")
        self.__debug_printer.newline()
        self.__debug_printer.enter()

    def leaveConst(self, node):
        self.__debug_printer.exit()

    def visitIdent(self, node):
        self.__debug_printer.append("Ident: " + node.data)
        self.__debug_printer.newline()

    def visitVar(self, node):
        self.__debug_printer.append("Var:")
        self.__debug_printer.newline()
        self.__debug_printer.enter()

    def leaveVar(self, node):
        self.__debug_printer.exit()

    def visitInt(self, node):
        self.__debug_printer.append("Int: " + str(node.data))
        self.__debug_printer.newline()
