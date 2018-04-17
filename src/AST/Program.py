
from AST.ASTNode import ASTNode


class Program(ASTNode):

    def __init__(self, lineNr, positionNr, includes, declarationList):
        super().__init__(lineNr, positionNr)
        self.includes = includes
        self.declarationList = declarationList

    def visit(self, visitorObject):
        return visitorObject("Program", [self.includes.visit(visitorObject), self.declarationList.visit(visitorObject)])

    def accept(self, listener):
        listener.enterProgram(self)
        self.includes.accept(listener)
        self.declarationList.accept(listener)
        listener.exitProgram(self)


class Includes(ASTNode):

    def __init__(self, lineNr, positionNr, includes):
        super().__init__(lineNr, positionNr)
        self.includes = includes    # list of Include nodes

    def visit(self, visitorObject):
        return visitorObject("Includes", [include.visit(visitorObject) for include in self.includes])

    def accept(self, listener):
        listener.enterIncludes(self)
        for include in self.includes:
            include.accept(listener)
        listener.exitIncludes(self)


class Include(ASTNode):

    def __init__(self, lineNr, positionNr, name):
        super().__init__(lineNr, positionNr)
        self.name = name    # string

    def visit(self, visitorObject):
        return visitorObject(self.name, [])

    def accept(self, listener):
        listener.enterInclude(self)
        listener.exitInclude(self)


class DeclarationList(ASTNode):

    def __init__(self, lineNr, positionNr, declarations):
        super().__init__(lineNr, positionNr)
        self.declarations = declarations    # list of Declaration nodes

    def visit(self, visitorObject):
        return visitorObject("Declarations", [declaration.visit(visitorObject) for declaration in self.declarations])

    def accept(self, listener):
        listener.enterDeclarationList(self)
        for declaration in self.declarations:
            declaration.accept(listener)
        listener.exitDeclarationList(self)
