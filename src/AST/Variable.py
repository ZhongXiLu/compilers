

class VariableDecl:

    def __init__(self, type, declList):
        self.type = type            # Type node
        self.declList = declList    # DeclList node?

    def visit(self, visitorObject):
        return visitorObject("VariableDecl", [self.type, self.declList.visit(visitorObject)])


class VarDeclList:

    def __init__(self, declInitializeList):
        self.declInitializeList = declInitializeList    # list of VarDeclInitialize nodes

    def visit(self, visitorObject):
        return visitorObject("VarDeclList", [declInit.visit(visitorObject) for declInit in self.declInitializeList])


class VarDeclInitialize:

    def __init__(self, name, expression=None):
        self.name = name                # string
        self.expression = expression    # Expression node

    def visit(self, visitorObject):
        if self.expression != None:
            return visitorObject("=", [self.name, self.expression.visit(visitorObject)])
        else:
            return visitorObject(self.name, [])
