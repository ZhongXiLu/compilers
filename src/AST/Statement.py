

class Compound:

    # TODO: add localDeclarations

    def __init__(self, statements):
        self.statements = statements     # list of Statement nodes

    def visit(self, visitorObject):
        return visitorObject("CompoundStmt", [stmt.visit(visitorObject) for stmt in self.statements])


class ExpressionStmt:

    def __init__(self, expression):
        self.expression = expression    # Expression node

    def visit(self, visitorObject):
        return visitorObject("ExpressionStmt", [self.expression.visit(visitorObject)])


class Return:

    def __init__(self, expression=None):
        self.expression = expression

    def visit(self, visitorObject):
        if self.expression is not None:
            return visitorObject("Return", [self.expression.visit(visitorObject)])
        else:
            return visitorObject("Return", [])


class If:

    def __init__(self, expression, body, elseBody=None):
        self.expression = expression    # Expression nodes
        self.body = body                # Statement node
        self.elseBody = elseBody        # Statement node (can be empty)

    def visit(self, visitorObject):
        if self.elseBody is not None:
            return visitorObject("IfStmt", [self.expression.visit(visitorObject), self.body.visit(visitorObject),
                                            self.elseBody.visit(visitorObject)])
        else:
            return visitorObject("IfStmt", [self.expression.visit(visitorObject), self.body.visit(visitorObject)])


class While:

    def __init__(self, expression, body):
        self.expression = expression    # Expression nodes
        self.body = body                # Statement node

    def visit(self, visitorObject):
        return visitorObject("While", [self.expression.visit(visitorObject), self.body.visit(visitorObject)])


class Break:

    def __init__(self):
        pass

    def visit(self, visitorObject):
        return visitorObject("Break", [])