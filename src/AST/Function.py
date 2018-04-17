

class FunctionDecl:

    def __init__(self, name, params, body, returns):
        self.name = name        # string
        self.params = params    # Parameters node
        self.body = body        # Compound node
        self.returns = returns  # type

    def visit(self, visitorObject):
        return visitorObject("FunctionDecl", [self.returns, self.name, self.params.visit(visitorObject),
                                              self.body.visit(visitorObject)])

    def accept(self, listener):
        listener.enterFunctionDecl(self)
        self.params.accept(listener)
        self.body.accept(listener)
        listener.exitFunctionDecl(self)


class Parameters:

    def __init__(self, params):
        self.params = params        # list of Parameter nodes

    def visit(self, visitorObject):
        return visitorObject("Parameters", [param.visit(visitorObject) for param in self.params])

    def accept(self, listener):
        listener.enterParameters(self)
        for param in self.params:
            param.accept(listener)
        listener.exitParameters(self)


class Parameter:

    def __init__(self, type, name):
        self.type = type    # string
        self.name = name    # string

    def visit(self, visitorObject):
        return visitorObject("Parameter", [self.type, self.name])

    def accept(self, listener):
        listener.enterParameter(self)
        listener.exitParameter(self)