

class FunctionDecl:

    def __init__(self, name, params, body, returns):
        self.name = name        # string
        self.params = params    # Parameters node
        self.body = body        # Compound node
        self.returns = returns  # type

    def visit(self, visitorObject):
        return visitorObject("FunctionDecl", [self.returns, self.name, self.params.visit(visitorObject),
                                              self.body.visit(visitorObject)])


class Parameters:

    def __init__(self, params):
        self.params = params        # list of Parameter nodes

    def visit(self, visitorObject):
        return visitorObject("Parameters", [param.visit(visitorObject) for param in self.params])


class Parameter:

    def __init__(self, type, name):
        self.type = type    # Type node
        self.name = name    # string

    def visit(self, visitorObject):
        return visitorObject("Parameter", [self.type, self.name])
