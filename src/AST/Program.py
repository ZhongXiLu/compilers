

class Program:

    def __init__(self, includes, declarationList):
        self.includes = includes
        self.declarationList = declarationList

    def visit(self, visitorObject):
        return visitorObject("Program", [self.includes.visit(visitorObject), self.declarationList.visit(visitorObject)])

    def accept(self, listener):
        listener.enterProgram(self)
        self.includes.accept(listener)
        self.declarationList.accept(listener)
        listener.exitProgram(self)


class Includes:

    def __init__(self, includes):
        self.includes = includes    # list of Include nodes

    def visit(self, visitorObject):
        return visitorObject("Includes", [include.visit(visitorObject) for include in self.includes])

    def accept(self, listener):
        listener.enterIncludes(self)
        for include in self.includes:
            include.accept(listener)
        listener.exitIncludes(self)


class Include:

    def __init__(self, name):
        self.name = name    # string

    def visit(self, visitorObject):
        return visitorObject(self.name, [])

    def accept(self, listener):
        listener.enterInclude(self)
        listener.exitInclude(self)


class DeclarationList:

    def __init__(self, declarations):
        self.declarations = declarations    # list of Declaration nodes

    def visit(self, visitorObject):
        return visitorObject("Declarations", [declaration.visit(visitorObject) for declaration in self.declarations])

    def accept(self, listener):
        listener.enterDeclarationList(self)
        for declaration in self.declarations:
            declaration.accept(listener)
        listener.exitDeclarationList(self)
