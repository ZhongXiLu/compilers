
from AST.ASTNode import ASTNode


class FunctionDef(ASTNode):

    def __init__(self, lineNr, positionNr, name, params, body, returns):
        super().__init__(lineNr, positionNr)
        self.name = name        # string
        self.params = params    # Parameters node
        self.body = body        # Compound node
        self.returns = returns  # type

    def visit(self, visitorObject):
        return visitorObject("FunctionDef", [self.returns, self.name, self.params.visit(visitorObject),
                                              self.body.visit(visitorObject)])

    def accept(self, listener):
        listener.enterFunctionDef(self)
        self.params.accept(listener)
        listener.enterFunctionBody(self)
        self.body.accept(listener)
        listener.exitFunctionDef(self)


class FunctionDecl(ASTNode):

    def __init__(self, lineNr, positionNr, name, params, returns):
        super().__init__(lineNr, positionNr)
        self.name = name        # string
        self.params = params    # Parameters node
        self.returns = returns  # type

    def visit(self, visitorObject):
        return visitorObject("FunctionDecl", [self.returns, self.name, self.params.visit(visitorObject)])

    def accept(self, listener):
        listener.enterFunctionDecl(self)
        self.params.accept(listener)
        listener.exitFunctionDecl(self)


class Parameters(ASTNode):

    def __init__(self, lineNr, positionNr, params):
        super().__init__(lineNr, positionNr)
        self.params = params        # list of Parameter nodes

    def visit(self, visitorObject):
        return visitorObject("Parameters", [param.visit(visitorObject) for param in self.params])

    def accept(self, listener):
        listener.enterParameters(self)
        for param in self.params:
            param.accept(listener)
        listener.exitParameters(self)


class Parameter(ASTNode):

    def __init__(self, lineNr, positionNr, type, name, size=None):
        super().__init__(lineNr, positionNr)
        self.type = type    # string
        self.name = name    # string
        self.size = size    # size for arrays

    def visit(self, visitorObject):
        if self.size is None:
            return visitorObject("Parameter", [self.type, self.name])
        else:
            return visitorObject("Parameter", [self.type, self.name, self.size])

    def accept(self, listener):
        listener.enterParameter(self)
        listener.exitParameter(self)