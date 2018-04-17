
from ASTListener import ASTListener
from SymbolTable.SymbolTable import SymbolTable


class SemanticValidator(ASTListener):

    def __init__(self):
        self.symbolTable = SymbolTable()
        self.errors = []

    def enterProgram(self, node):
        self.symbolTable.newScope()

    def exitProgram(self, node):
        self.symbolTable.endScope()

    def enterCompound(self, node):
        self.symbolTable.newScope()

    def exitCompound(self, node):
        self.symbolTable.endScope()

    def enterVariableDecl(self, node):
        declList = node.declList
        for varDeclInit in declList.declInitializeList:
            # Check if new var already exists in current scope
            symbolInfo = self.symbolTable.getSymbolInCurrentScope(varDeclInit.name)
            if symbolInfo is None:
                self.symbolTable.addSymbol(varDeclInit.name, node.type)
            else:
                self.errors.append("Redefinition of '" + varDeclInit.name + "'")

    def enterCall(self, node):
        symbolInfo = self.symbolTable.getSymbol(node.funcName)
        if symbolInfo is None or symbolInfo != "function":  # TODO: make FunctionInfo
            if node.funcName != "printf" and node.funcName != "scanf":
                self.errors.append("Undefined reference to '" + node.funcName + "'")

    def enterMutable(self, node):
        symbolInfo = self.symbolTable.getSymbol(node.name)
        if symbolInfo is None or symbolInfo == "function":  # TODO: make VarInfo
            self.errors.append("Undefined reference to '" + node.name + "'")

    def enterFunctionDecl(self, node):
        # Check if new function already exists
        symbolInfo = self.symbolTable.getSymbol(node.name)
        if symbolInfo is None:
            self.symbolTable.addSymbol(node.name, "function")
            self.symbolTable.newScope()

            params = node.params
            for param in params.params:
                self.symbolTable.addSymbol(param.name, param.type)
        else:
            self.errors.append("Redefinition of '" + node.name + "'")

    def exitFunctionDecl(self, node):
        self.symbolTable.endScope()
