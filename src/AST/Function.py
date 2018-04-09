

class Function:

    def __init__(self, name, args, body, returns):
        self.name = name        # string
        self.args = args        # list of Argument nodes
        self.body = body        # list of nodes
        self.returns = returns  # type

    def visit(self, visitorObject):
        items = []
        # [items.append(arg.visit(visitorObject)) for arg in self.args]
        # [items.append(node.visit(visitorObject)) for node in self.body]
        return visitorObject("Function", [self.returns, self.name] + items)

class Argument:

    def __init__(self, type, name):
        self.type = type    # Type node
        self.name = name    # string
