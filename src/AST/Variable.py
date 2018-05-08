
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
        self.declInitializeList = declInitializeList    # list of VarDeclInitialize/ArrayInitialize nodes

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


class ArrayInitialize(ASTNode):

    def __init__(self, lineNr, positionNr, name, size, initialize=None):
        super().__init__(lineNr, positionNr)
        self.name = name                # string
        self.size = size                # int
        self.initialize = initialize    # ArrayInitializeList node

    def visit(self, visitorObject):
        if self.initialize is not None:
            return visitorObject("ArrayInitialize", [self.name, self.size, self.initialize.visit(visitorObject)])
        else:
            return visitorObject("ArrayInitialize", [self.name, self.size])

    def accept(self, listener):
        listener.enterArrayInitialize(self)
        self.initialize.accept(listener)
        listener.exitArrayInitialize(self)


class ArrayInitializeList(ASTNode):

    def __init__(self, lineNr, positionNr, initializeList=[]):
        super().__init__(lineNr, positionNr)
        self.list = initializeList    # list of Expression nodes

    def visit(self, visitorObject):
        return visitorObject("ArrayInitializeList", [init.visit(visitorObject) for init in self.list])

    def accept(self, listener):
        listener.enterArrayInitializeList(self)
        for initialize in self.list:
            initialize.accept(listener)
        listener.exitArrayInitializeList(self)
