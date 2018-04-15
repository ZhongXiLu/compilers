
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
        self.operator = operator    # BinOpToken
        self.operand = operand      # Expression node

    def visit(self, visitorObject):
        return visitorObject(self.operator.value, [self.operand.visit(visitorObject)])