

class Program:

    def __init__(self, includes, declarationList):
        self.includes = includes
        self.declarationList = declarationList

    def visit(self, visitorObject):
        return visitorObject("Program", [self.includes.visit(visitorObject), self.declarationList.visit(visitorObject)])


class Includes:

    def __init__(self, includes):
        self.includes = includes    # list of Include nodes

    def visit(self, visitorObject):
        return visitorObject("Includes", [include.visit(visitorObject) for include in self.includes])


class Include:

    def __init__(self, name):
        self.name = name    # string

    def visit(self, visitorObject):
        return visitorObject(self.name, [])


class DeclarationList:

    def __init__(self, declarations):
        self.declarations = declarations    # list of Declaration nodes

    def visit(self, visitorObject):
        return visitorObject("Declarations", [declaration.visit(visitorObject) for declaration in self.declarations])
