
from ASTListener import ASTListener
from SymbolTable.SymbolTable import *
from AST import Expression, Function, Literals, Program, Statement, Variable


class CodeGenerator(ASTListener):

    def __init__(self, symbolTable, file="p_prog.p"):
        self.symbolTable = symbolTable
        self.nextFreeAddress = 0        # = environment
        self.file = open(file, "w")

    def getFreeAddress(self):
        self.nextFreeAddress += 1
        return self.nextFreeAddress - 1

    def isCharType(self, type):
        if type == "char" or type == "char*":
            return True
        else:
            return False

    def enterProgram(self, node):
        self.symbolTable.reset()
        self.symbolTable.currentScope = self.symbolTable.currentScope.getNextScope()

    def exitProgram(self, node):
        self.file.write("hlt\n")
        self.file.close()

        self.symbolTable.currentScope = self.symbolTable.currentScope.parent

    def enterCompound(self, node):
        self.symbolTable.currentScope = self.symbolTable.currentScope.getNextScope()

    def exitCompound(self, node):
        self.symbolTable.currentScope = self.symbolTable.currentScope.parent

    def enterFunctionDef(self, node):
        self.symbolTable.currentScope = self.symbolTable.currentScope.getNextScope()

    def exitFunctionDef(self, node):
        self.symbolTable.currentScope = self.symbolTable.currentScope.parent

    def enterVarDeclInitialize(self, node):
        # Initialize variable with default value
        self.symbolTable.getSymbol(node.name).address = self.getFreeAddress()
        if self.isCharType(self.symbolTable.getSymbol(node.name).type):
            self.file.write("ldc c ' '\n")
        else:
            self.file.write("ldc i 0\n")

    def exitVarDeclInitialize(self, node):
        # Overwrite value with the actual initialized value, if any
        if node.expression is not None:
            # => top of stack is result of expression (= initialized value)
            if self.isCharType(self.symbolTable.getSymbol(node.name).type):
                self.file.write("sro c " + str(self.symbolTable.getSymbol(node.name).address) + "\n")
            else:
                self.file.write("sro i " + str(self.symbolTable.getSymbol(node.name).address) + "\n")
