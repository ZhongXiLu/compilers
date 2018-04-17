
from AST.ASTNode import ASTNode
from enum import Enum


class BinOpTokens(Enum):
    AND = "&&"
    OR = "||"
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="
    EQ = "=="
    NEQ = "!="
    PLUS = "+"
    MIN = "-"
    MULT = "*"
    DIV = "/"


class UnaryOpTokens(Enum):
    NEG = "!"
    MIN = "-"


class Assign(ASTNode):

    def __init__(self, lineNr, positionNr, left, right):
        super().__init__(lineNr, positionNr)
        self.left = left            # Mutable node
        self.right = right          # Expression node

    def visit(self, visitorObject):
        return visitorObject("=", [self.left.visit(visitorObject), self.right.visit(visitorObject)])

    def accept(self, listener):
        listener.enterAssign(self)
        self.left.accept(listener)
        self.right.accept(listener)
        listener.exitAssign(self)


class BinOp(ASTNode):

    def __init__(self, lineNr, positionNr, operator, left, right):
        super().__init__(lineNr, positionNr)
        self.operator = operator    # BinOpToken
        self.left = left            # Expression node
        self.right = right          # Expression node

    def visit(self, visitorObject):
        return visitorObject(self.operator.value, [self.left.visit(visitorObject), self.right.visit(visitorObject)])

    def accept(self, listener):
        listener.enterBinOp(self)
        self.left.accept(listener)
        self.right.accept(listener)
        listener.exitBinOp(self)


class UnaryOp(ASTNode):

    def __init__(self, lineNr, positionNr, operator, operand):
        super().__init__(lineNr, positionNr)
        self.operator = operator    # UnaryOpToken
        self.operand = operand      # Expression node

    def visit(self, visitorObject):
        return visitorObject(self.operator.value, [self.operand.visit(visitorObject)])

    def accept(self, listener):
        listener.enterUnaryOp(self)
        self.operand.accept(listener)
        listener.enterUnaryOp(self)


class Call(ASTNode):

    def __init__(self, lineNr, positionNr, funcName, args):
        super().__init__(lineNr, positionNr)
        self.funcName = funcName    # string
        self.args = args            # list of expressions

    def visit(self, visitorObject):
        return visitorObject(self.funcName, [arg.visit(visitorObject) for arg in self.args])

    def accept(self, listener):
        listener.enterCall(self)
        for arg in self.args:
            arg.accept(listener)
        listener.exitCall(self)


class Mutable(ASTNode):

    def __init__(self, lineNr, positionNr, name):
        super().__init__(lineNr, positionNr)
        self.name = name    # string

    def visit(self, visitorObject):
        return visitorObject(self.name, [])

    def accept(self, listener):
        listener.enterMutable(self)
        listener.exitMutable(self)


class SubScript(ASTNode):

    def __init__(self, lineNr, positionNr, mutable, index):
        super().__init__(lineNr, positionNr)
        self.mutable = mutable  # Mutable node
        self.index = index      # Expression node

    def visit(self, visitorObject):
        return visitorObject("[]", [self.mutable.visit(visitorObject), self.index.visit(visitorObject)])

    def accept(self, listener):
        listener.enterSubScript(self)
        self.mutable.accept(listener)
        self.index.accept(listener)
        listener.exitSubScript(self)

