

class Compound:

    # TODO: add localDeclarations

    def __init__(self, statements):
        self.statements = statements     # list of Argument nodes

    def visit(self, visitorObject):
        return visitorObject("CompoundStmt", [stmt.visit(visitorObject) for stmt in self.statements])


class Return:

    def __init__(self, expression=None):
        self.expression = expression

    def visit(self, visitorObject):
        if self.expression is not None:
            return visitorObject("Return", ["TODO: expression"])
            # return visitorObject("Return", [self.expression.visit(visitorObject)])
        else:
            return visitorObject("Return", [])
