class Visitor:
    def __init__(self):
        self.__visitors = {}
        self.__leavers = {}

    def visit(self, name, node):
        for (node_name, visitor) in self.__visitors.items():
            if node_name == name:
                if visitor(node) is False:
                    return False

    def leave(self, name, node):
        for (node_name, leaver) in self.__leavers.items():
            if node_name == name:
                leaver(node)

    def add_visitor(self, name, visitor):
        assert callable(visitor), "visitor callback must be callable, not {type(visitor)}"  # noqa
        self.__visitors[name] = visitor

    def add_leaver(self, name, leaver):
        assert callable(leaver), "visitor callback must be callable, not {type(leaver)}"  # noqa
        self.__leavers[name] = leaver
