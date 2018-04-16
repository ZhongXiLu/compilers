
from enum import Enum


class BinOpTokens(Enum):
    ASSIGN = "="
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


class Expression:

    def __init__(self):
        pass

    def visit(self, visitorObject):
        return visitorObject("TODO: Expression", [])


class SimpleExpression:

    def __init__(self):
        pass

    def visit(self, visitorObject):
        return visitorObject("TODO: SimpleExpression", [])


class BinOp:

    def __init__(self, operator, left, right):
        self.operator = operator    # BinOpToken
        self.left = left            # Expression node
        self.right = right          # Expression node

    def visit(self, visitorObject):
        return visitorObject(self.operator.value, [self.left.visit(visitorObject), self.right.visit(visitorObject)])


class UnaryOp:

    def __init__(self, operator, operand):
        self.operator = operator    # UnaryOpToken
        self.operand = operand      # Expression node

    def visit(self, visitorObject):
        return visitorObject(self.operator.value, [self.operand.visit(visitorObject)])


class Call:

    def __init__(self, funcName, args):
        self.funcName = funcName    # string
        self.args = args            # list of expressions

    def visit(self, visitorObject):
        return visitorObject(self.funcName, [arg.visit(visitorObject) for arg in self.args])


class Mutable:

    def __init__(self, name):
        self.name = name    # string

    def visit(self, visitorObject):
        return visitorObject(self.name, [])


class SubScript:

    def __init__(self, mutable, index):
        self.mutable = mutable  # Mutable node
        self.index = index      # Expression node

    def visit(self, visitorObject):
        return visitorObject("[]", [self.mutable.visit(visitorObject), self.index.visit(visitorObject)])

