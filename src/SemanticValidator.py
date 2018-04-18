
from ASTListener import ASTListener
from SymbolTable.SymbolTable import *
from AST import Expression, Function, Literals, Program, Statement, Variable


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
                if type(node) is Variable.VarDeclInitialize:
                    self.symbolTable.addSymbol(varDeclInit.name, VarInfo(node.type))
                else:
                    self.symbolTable.addSymbol(varDeclInit.name, ArrayInfo(node.type, varDeclInit.size))
            else:
                self.errors.append(varDeclInit.getPosition() + ": Redefinition of '" + varDeclInit.name + "'")

    def enterCall(self, node):
        symbolInfo = self.symbolTable.getSymbol(node.funcName)
        if symbolInfo is None or type(symbolInfo) is not FunctionInfo:
            if node.funcName != "printf" and node.funcName != "scanf":
                self.errors.append(node.getPosition() + ": Undefined reference to '" + node.funcName + "'")

        else:
            # TODO: Check if params match the function declaration
            for arg in node.args:
                pass

    def enterMutable(self, node):
        symbolInfo = self.symbolTable.getSymbol(node.name)
        if symbolInfo is None or (type(symbolInfo) is not VarInfo and type(symbolInfo) is not ArrayInfo):
            self.errors.append(node.getPosition() + ": Undefined reference to '" + node.name + "'")

    def enterSubScript(self, node):
        symbolInfo = self.symbolTable.getSymbol(node.mutable.name)
        if symbolInfo is None or type(symbolInfo) is not ArrayInfo:
            self.errors.append(node.getPosition() + ": Subscripted value '" + node.mutable.name + "' is not an array")
        else:
            # TODO Check if in bounds
            index = 0
            if index > 0 and 0 < symbolInfo.size:
                pass

    def enterFunctionDecl(self, node):
        # Check if new function already exists
        symbolInfo = self.symbolTable.getSymbol(node.name)
        if symbolInfo is None:
            params = node.params
            paramTypes = []
            for param in params.params:
                paramTypes.append(param.type)
                self.symbolTable.addSymbol(param.name, VarInfo(param.type))

            self.symbolTable.addSymbol(node.name, FunctionInfo(node.returns, paramTypes))
            self.symbolTable.newScope()

        else:
            self.errors.append(node.getPosition() + ": Redefinition of '" + node.name + "'")

    def exitFunctionDecl(self, node):
        self.symbolTable.endScope()
