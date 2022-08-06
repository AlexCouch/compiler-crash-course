from dataclasses import dataclass
from token_pos import TokenPositionRange

@dataclass
class ASTNode:
    name: str
    pos: TokenPositionRange
    children: 'list[ASTNode]'
    data: any
    container: bool

    #
    # CONSTRUCTORS
    #

    @staticmethod
    def new(name, pos, data, container):
        return ASTNode(name, pos, [], data, container)

    @staticmethod
    def container(name, pos):
        return ASTNode(name, pos, [], None, True)

    @staticmethod
    def file(path):
        return ASTNode.new('file', None, path, True)

    @staticmethod
    def const(pos):
        return ASTNode.container('const', pos)

    @staticmethod
    def variable(pos):
        return ASTNode.container('var', pos)

    @staticmethod
    def integer(pos, value):
        return ASTNode.new('int', pos, value, False)

    @staticmethod
    def ident(pos, value):
        return ASTNode.new('ident', pos, value, False)

    @staticmethod
    def refvar(name, pos):
        return ASTNode.new('refvar', pos, name, False)

    @staticmethod
    def mut(pos):
        return ASTNode.container('mut', pos)


    # METHODS

    def to_container(self):
        return ASTNode.new(self.name, self.pos, [], self.data)

    def match(self, name):
        return self.name == name

    def contains(self, pred):
        return pred(self.data)

    def add_child(self, child):
        if not self.is_container():
            print("Node is not a container")
            return False
        assert isinstance(child, ASTNode), f"Child must be of type 'ASTNode' not type {type(child)}"  # noqa
        self.children.append(child)
        return True

    def is_container(self):
        return self.container

    def accept(self, visitor):
        if visitor.visit(self.name, self) is False:
            return False
        if self.is_container():
            for child in self.children:
                if child.accept(visitor) is False:
                    return False
        if visitor.leave(self.name, self) is False:
            return False
