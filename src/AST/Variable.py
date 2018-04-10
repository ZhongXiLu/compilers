

class VariableDecl:

    def __init__(self, type, declList):
        self.type = type            # Type node
        self.declList = declList    # DeclList node?

    def visit(self, visitorObject):
        return visitorObject("VariableDecl", [self.type, self.name])
