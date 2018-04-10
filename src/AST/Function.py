

class FunctionDecl:

    def __init__(self, name, args, body, returns):
        self.name = name        # string
        self.args = args        # Arguments node
        self.body = body        # Compound node
        self.returns = returns  # type

    def visit(self, visitorObject):
        return visitorObject("FunctionDecl", [self.returns, self.name, self.args.visit(visitorObject), self.body.visit(visitorObject)])


class Arguments:

    def __init__(self, args):
        self.args = args        # list of Argument nodes

    def visit(self, visitorObject):
        return visitorObject("Arguments", [arg.visit(visitorObject) for arg in self.args])


class Argument:

    def __init__(self, type, name):
        self.type = type    # Type node
        self.name = name    # string

    def visit(self, visitorObject):
        return visitorObject("Argument", [self.type, self.name])
