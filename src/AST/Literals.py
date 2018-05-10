
from AST.ASTNode import ASTNode


class Int(ASTNode):

    def __init__(self, lineNr, positionNr, value):
        super().__init__(lineNr, positionNr)
        self.value = value

    def visit(self, visitorObject):
        return visitorObject(self.value, [])

    def accept(self, listener):
        listener.enterInt(self)
        listener.exitInt(self)


class Double(ASTNode):

    def __init__(self, lineNr, positionNr, value):
        super().__init__(lineNr, positionNr)
        self.value = value

    def visit(self, visitorObject):
        return visitorObject(self.value, [])

    def accept(self, listener):
        listener.enterDouble(self)
        listener.exitDouble(self)


class String(ASTNode):

    def __init__(self, lineNr, positionNr, value):
        super().__init__(lineNr, positionNr)
        self.value = value

    def visit(self, visitorObject):
        return visitorObject(self.value, [])

    def accept(self, listener):
        listener.enterString(self)
        listener.exitString(self)


class Char(ASTNode):

    def __init__(self, lineNr, positionNr, value):
        super().__init__(lineNr, positionNr)
        self.value = value

    def visit(self, visitorObject):
        return visitorObject(self.value, [])

    def accept(self, listener):
        listener.enterChar(self)
        listener.exitChar(self)
