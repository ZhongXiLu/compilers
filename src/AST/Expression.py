
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


class Assign:

    def __init__(self, left, right):
        self.left = left            # Mutable node
        self.right = right          # Expression node

    def visit(self, visitorObject):
        return visitorObject("=", [self.left.visit(visitorObject), self.right.visit(visitorObject)])

    def accept(self, listener):
        listener.enterAssign(self)
        self.left.accept(listener)
        self.right.accept(listener)
        listener.exitAssign(self)


class BinOp:

    def __init__(self, operator, left, right):
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


class UnaryOp:

    def __init__(self, operator, operand):
        self.operator = operator    # UnaryOpToken
        self.operand = operand      # Expression node

    def visit(self, visitorObject):
        return visitorObject(self.operator.value, [self.operand.visit(visitorObject)])

    def accept(self, listener):
        listener.enterUnaryOp(self)
        self.operand.accept(listener)
        listener.enterUnaryOp(self)


class Call:

    def __init__(self, funcName, args):
        self.funcName = funcName    # string
        self.args = args            # list of expressions

    def visit(self, visitorObject):
        return visitorObject(self.funcName, [arg.visit(visitorObject) for arg in self.args])

    def accept(self, listener):
        listener.enterCall(self)
        for arg in self.args:
            arg.accept(listener)
        listener.exitCall(self)


class Mutable:

    def __init__(self, name):
        self.name = name    # string

    def visit(self, visitorObject):
        return visitorObject(self.name, [])

    def accept(self, listener):
        listener.enterMutable(self)
        listener.exitMutable(self)


class SubScript:

    def __init__(self, mutable, index):
        self.mutable = mutable  # Mutable node
        self.index = index      # Expression node

    def visit(self, visitorObject):
        return visitorObject("[]", [self.mutable.visit(visitorObject), self.index.visit(visitorObject)])

    def accept(self, listener):
        listener.enterSubScript(self)
        self.mutable.accept(listener)
        self.index.accept(listener)
        listener.exitSubScript(self)

