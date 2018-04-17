
from AST.ASTNode import ASTNode


class Number(ASTNode):

    def __init__(self, lineNr, positionNr, number):
        super().__init__(lineNr, positionNr)
        self.number = number

    def visit(self, visitorObject):
        return visitorObject(self.number, [])

    def accept(self, listener):
        listener.enterNumber(self)
        listener.exitNumber(self)


class String(ASTNode):

    def __init__(self, lineNr, positionNr, string):
        super().__init__(lineNr, positionNr)
        self.string = string

    def visit(self, visitorObject):
        return visitorObject(self.string, [])

    def accept(self, listener):
        listener.enterString(self)
        listener.exitString(self)
