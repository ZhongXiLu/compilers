

class Function:

    def __init__(self, name, args, body, returns):
        self.name = name        # string
        self.args = args        # list of Argument nodes
        self.body = body        # list of nodes
        self.returns = returns  # type

    def visit(self, visitorObject):
        items = []
        # [items.append(node.visit(visitorObject)) for node in self.body]
        return visitorObject("Function", [self.returns, self.name, self.args.visit(visitorObject)] + items)


class Arguments:

    def __init__(self, args):
        self.args = args        # list of Argument nodes

    def visit(self, visitorObject):
        items = []
        [items.append(arg.visit(visitorObject)) for arg in self.args]
        return visitorObject("Arguments", items)


class Argument:

    def __init__(self, type, name):
        self.type = type    # Type node
        self.name = name    # string

    def visit(self, visitorObject):
        return visitorObject("Argument", [self.type, self.name])
