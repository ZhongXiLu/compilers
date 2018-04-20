
from AST.ASTNode import ASTNode


class Int(ASTNode):

    def __init__(self, lineNr, positionNr, _int):
        super().__init__(lineNr, positionNr)
        self._int = _int

    def visit(self, visitorObject):
        return visitorObject(self._int, [])

    def accept(self, listener):
        listener.enterInt(self)
        listener.exitInt(self)


class Double(ASTNode):

    def __init__(self, lineNr, positionNr, double):
        super().__init__(lineNr, positionNr)
        self.double = double

    def visit(self, visitorObject):
        return visitorObject(self.double, [])

    def accept(self, listener):
        listener.enterDouble(self)
        listener.exitDouble(self)


class String(ASTNode):

    def __init__(self, lineNr, positionNr, string):
        super().__init__(lineNr, positionNr)
        self.string = string

    def visit(self, visitorObject):
        return visitorObject(self.string, [])

    def accept(self, listener):
        listener.enterString(self)
        listener.exitString(self)


class Char(ASTNode):

    def __init__(self, lineNr, positionNr, char):
        super().__init__(lineNr, positionNr)
        self.char = char

    def visit(self, visitorObject):
        return visitorObject(self.char, [])

    def accept(self, listener):
        listener.enterChar(self)
        listener.exitChar(self)
