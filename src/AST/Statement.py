
from AST.ASTNode import ASTNode


class Compound(ASTNode):

    def __init__(self, lineNr, positionNr, localDecls=[], statements=[]):
        super().__init__(lineNr, positionNr)
        self.localDecls = localDecls     # list of VariableDecl nodes
        self.statements = statements     # list of Statement nodes

    def visit(self, visitorObject):
        return visitorObject("CompoundStmt", [decl.visit(visitorObject) for decl in self.localDecls] +
                             [stmt.visit(visitorObject) for stmt in self.statements])

    def accept(self, listener):
        listener.enterCompound(self)
        for declaration in self.localDecls:
            declaration.accept(listener)
        for statement in self.statements:
            statement.accept(listener)
        listener.exitCompound(self)


class ExpressionStmt(ASTNode):

    def __init__(self, lineNr, positionNr, expression):
        super().__init__(lineNr, positionNr)
        self.expression = expression    # Expression node

    def visit(self, visitorObject):
        return visitorObject("ExpressionStmt", [self.expression.visit(visitorObject)])

    def accept(self, listener):
        listener.enterExpressionStmt(self)
        self.expression.accept(listener)
        listener.exitExpressionStmt(self)


class Return(ASTNode):

    def __init__(self, lineNr, positionNr, expression=None):
        super().__init__(lineNr, positionNr)
        self.expression = expression

    def visit(self, visitorObject):
        if self.expression is not None:
            return visitorObject("Return", [self.expression.visit(visitorObject)])
        else:
            return visitorObject("Return", [])

    def accept(self, listener):
        listener.enterReturn(self)
        if self.expression is not None:
            self.expression.accept(listener)
        listener.exitReturn(self)


class If(ASTNode):

    def __init__(self, lineNr, positionNr, expression, body, elseBody=None):
        super().__init__(lineNr, positionNr)
        self.expression = expression    # Expression node
        self.body = body                # Statement node
        self.elseBody = elseBody        # Statement node (can be empty)

    def visit(self, visitorObject):
        if self.elseBody is not None:
            return visitorObject("IfStmt", [self.expression.visit(visitorObject), self.body.visit(visitorObject),
                                            self.elseBody.visit(visitorObject)])
        else:
            return visitorObject("IfStmt", [self.expression.visit(visitorObject), self.body.visit(visitorObject)])

    def accept(self, listener):
        listener.enterIf(self)
        self.expression.accept(listener)
        self.body.accept(listener)
        if self.elseBody is not None:
            self.elseBody.accept(listener)
        listener.exitIf(self)


class While(ASTNode):

    def __init__(self, lineNr, positionNr, expression, body):
        super().__init__(lineNr, positionNr)
        self.expression = expression    # Expression nodes
        self.body = body                # Statement node

    def visit(self, visitorObject):
        return visitorObject("While", [self.expression.visit(visitorObject), self.body.visit(visitorObject)])

    def accept(self, listener):
        listener.enterWhile(self)
        self.expression.accept(listener)
        self.body.accept(listener)
        listener.exitWhile(self)


class Break(ASTNode):

    def __init__(self, lineNr, positionNr):
        super().__init__(lineNr, positionNr)
        pass

    def visit(self, visitorObject):
        return visitorObject("Break", [])

    def accept(self, listener):
        listener.enterBreak(self)
        listener.exitBreak(self)