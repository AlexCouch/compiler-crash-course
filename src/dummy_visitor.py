from visitor import Visitor

class DummyVisitor:
    def __init__(self):
        self.__visitor = Visitor()
        self.__visitor.add_visitor('file', self.dummy_visit)
        self.__visitor.add_visitor('var', self.dummy_visit)
        self.__visitor.add_visitor('ident', self.dummy_visit)
        self.__visitor.add_visitor('int', self.dummy_visit)

    def dummy_visit(self, node):
        pass

    def visit(self, node):
        node.accept(self.__visitor)
