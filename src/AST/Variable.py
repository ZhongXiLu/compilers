
from AST.ASTNode import ASTNode


class VariableDecl(ASTNode):

    def __init__(self, lineNr, positionNr, type, declList):
        super().__init__(lineNr, positionNr)
        self.type = type
        self.declList = declList    # VarDeclList node

    def visit(self, visitorObject):
        return visitorObject("VariableDecl", [self.type, self.declList.visit(visitorObject)])

    def accept(self, listener):
        listener.enterVariableDecl(self)
        self.declList.accept(listener)
        listener.exitVariableDecl(self)


class VarDeclList(ASTNode):

    def __init__(self, lineNr, positionNr, declInitializeList):
        super().__init__(lineNr, positionNr)
        self.declInitializeList = declInitializeList    # list of VarDeclInitialize nodes

    def visit(self, visitorObject):
        return visitorObject("VarDeclList", [declInit.visit(visitorObject) for declInit in self.declInitializeList])

    def accept(self, listener):
        listener.enterVarDeclList(self)
        for initialize in self.declInitializeList:
            initialize.accept(listener)
        listener.exitVarDeclList(self)


class VarDeclInitialize(ASTNode):

    def __init__(self, lineNr, positionNr, name, expression=None):
        super().__init__(lineNr, positionNr)
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
