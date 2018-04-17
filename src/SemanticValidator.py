
from ASTListener import ASTListener
from SymbolTable.SymbolTable import SymbolTable


class SemanticValidator(ASTListener):

    def __init__(self):
        self.symbolTable = SymbolTable()

    def enterVariableDecl(self, node):
        print(node.type)    # test