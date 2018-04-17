

class VariableDecl:

    def __init__(self, type, declList):
        self.type = type
        self.declList = declList    # VarDeclList node

    def visit(self, visitorObject):
        return visitorObject("VariableDecl", [self.type, self.declList.visit(visitorObject)])

    def accept(self, listener):
        listener.enterVariableDecl(self)
        self.declList.accept(listener)
        listener.exitVariableDecl(self)


class VarDeclList:

    def __init__(self, declInitializeList):
        self.declInitializeList = declInitializeList    # list of VarDeclInitialize nodes

    def visit(self, visitorObject):
        return visitorObject("VarDeclList", [declInit.visit(visitorObject) for declInit in self.declInitializeList])

    def accept(self, listener):
        listener.enterVarDeclList(self)
        for initialize in self.declInitializeList:
            initialize.accept(listener)
        listener.exitVarDeclList(self)


class VarDeclInitialize:

    def __init__(self, name, expression=None):
        self.name = name                # string
        self.expression = expression    # Expression node

    def visit(self, visitorObject):
        if self.expression != None:
            return visitorObject("=", [self.name, self.expression.visit(visitorObject)])
        else:
            return visitorObject(self.name, [])

    def accept(self, listener):
        listener.enterVarDeclInitialize(self)
        if self.expression != None:
            self.expression.accept(listener)
        listener.exitVarDeclInitialize(self)
