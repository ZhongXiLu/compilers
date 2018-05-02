
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

    def getPType(self, type):
        if type == "char" or type == "char*":
            return "c"
        elif type == "double" or type == "double*" or type == "float" or type == "float*":
            return "r"
        else:
            return "i"

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
        if self.getPType(self.symbolTable.getSymbol(node.name).type) == "c":
            self.file.write("ldc c ' '\n")
        elif self.getPType(self.symbolTable.getSymbol(node.name).type) == "r":
            self.file.write("ldc r 0.0\n")
        else:
            self.file.write("ldc i 0\n")

    def exitVarDeclInitialize(self, node):
        # Overwrite value with the actual initialized value, if any
        if node.expression is not None:
            # => top of stack is result of expression (= initialized value)
            symbol = self.symbolTable.getSymbol(node.name)
            self.file.write("sro " + self.getPType(symbol.type) + " " + str(symbol.address) + "\n")

    def enterInt(self, node):
        self.file.write("ldc i " + str(node._int) + "\n")

    def enterDouble(self, node):
        self.file.write("ldc r " + str(node.double) + "\n")

    def enterString(self, node):
        self.file.write("ldc c " + str(node.string) + "\n")

    def enterChar(self, node):
        self.file.write("ldc c " + str(node.char) + "\n")

    def exitAssign(self, node):
        symbol = self.symbolTable.getSymbol(node.left.name)
        self.file.write("sro " + self.getPType(symbol.type) + " " + str(symbol.address) + "\n")
