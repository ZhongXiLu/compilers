
from ASTListener import ASTListener
from SymbolTable.SymbolTable import *
from AST import Expression, Function, Literals, Program, Statement, Variable
from SemanticValidator import SemanticValidator, getType


class CodeGenerator(ASTListener):

    # TODO: free variables after endScope?

    def __init__(self, symbolTable, file="p_prog.p"):
        self.symbolTable = symbolTable
        self.nextFreeAddress = 5        # = environment
        self.labelId = 0

        # Temporary variables
        self.endLabel = None        # temporary store label names to use for later
        self.elseLabel = None
        self.startLabel = None
        self.isAssignee = False     # small hack to make sure mutables arent printed on lhs

        self.file = open(file, "w")


    def getFreeAddress(self):
        self.nextFreeAddress += 1
        return self.nextFreeAddress - 1

    def getFreeLabel(self):
        self.labelId += 1
        return "l" + str(self.labelId - 1)

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
        self.file.write("ssp 5\n")
        # TODO: ...
        self.file.write("ujp main\n")

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

        if node.name != "main":
            self.file.write("spp " + str(len(node.params.params)) + "\n")   # TODO: correct?
            # TODO: ...
            self.file.write("ujp " + node.name + "\n")

    def enterFunctionBody(self, node):
        self.file.write(node.name + ":" + "\n")

    def exitFunctionDef(self, node):
        if node.name != "main":
            if node.returns != "void":
                self.file.write("retf\n")   # result in local stack
            else:
                self.file.write("retp\n")
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

    def enterMutable(self, node):
        if not self.isAssignee:
            symbol = self.symbolTable.getSymbol(node.name)
            self.file.write("ldo " + self.getPType(symbol.type) + " " + str(symbol.address) + "\n")
        else:
            self.isAssignee = False

    def enterInt(self, node):
        self.file.write("ldc i " + str(node._int) + "\n")

    def enterDouble(self, node):
        self.file.write("ldc r " + str(node.double) + "\n")

    def enterString(self, node):
        self.file.write("ldc c " + str(node.string) + "\n")

    def enterChar(self, node):
        self.file.write("ldc c " + str(node.char) + "\n")

    def enterAssign(self, node):
        self.isAssignee = True

    def exitAssign(self, node):
        symbol = self.symbolTable.getSymbol(node.left.name)
        self.file.write("sro " + self.getPType(symbol.type) + " " + str(symbol.address) + "\n")

    def exitBinOp(self, node):
        # Arithmetic
        if node.operator == Expression.BinOpTokens.PLUS:
            self.file.write("add " + self.getPType(getType(node, "", self.symbolTable)[0]) + "\n")
        elif node.operator == Expression.BinOpTokens.MIN:
            self.file.write("sub " + self.getPType(getType(node, "", self.symbolTable)[0]) + "\n")
        elif node.operator == Expression.BinOpTokens.MULT:
            self.file.write("mul " + self.getPType(getType(node, "", self.symbolTable)[0]) + "\n")
        elif node.operator == Expression.BinOpTokens.DIV:
            self.file.write("div " + self.getPType(getType(node, "", self.symbolTable)[0]) + "\n")

        # Comparison
        elif node.operator == Expression.BinOpTokens.LT:
            self.file.write("les " + self.getPType(getType(node, "", self.symbolTable)[0]) + "\n")
        elif node.operator == Expression.BinOpTokens.GT:
            self.file.write("grt " + self.getPType(getType(node, "", self.symbolTable)[0]) + "\n")
        elif node.operator == Expression.BinOpTokens.LTE:
            self.file.write("leq " + self.getPType(getType(node, "", self.symbolTable)[0]) + "\n")
        elif node.operator == Expression.BinOpTokens.GTE:
            self.file.write("geq " + self.getPType(getType(node, "", self.symbolTable)[0]) + "\n")
        elif node.operator == Expression.BinOpTokens.EQ:
            self.file.write("equ " + self.getPType(getType(node, "", self.symbolTable)[0]) + "\n")
        elif node.operator == Expression.BinOpTokens.NEQ:
            self.file.write("neq " + self.getPType(getType(node, "", self.symbolTable)[0]) + "\n")

        # Logical
        elif node.operator == Expression.BinOpTokens.AND:
            self.file.write("and\n")
        elif node.operator == Expression.BinOpTokens.OR:
            self.file.write("or\n")

    def enterIfBranch(self, node):
        # Make sure expression is evaluated first
        if node.elseBody is None:
            self.endLabel = self.getFreeLabel()
            self.file.write("fjp " + self.endLabel + "\n")      # jump to end
        else:
            self.elseLabel = self.getFreeLabel()
            self.file.write("fjp " + self.elseLabel + "\n")     # jump to else branch

    def enterElseBranch(self, node):
        self.endLabel = self.getFreeLabel()
        self.file.write("ujp " + self.endLabel + "\n")      # end of if branch -> jump to end
        self.file.write(self.elseLabel + ":" + "\n")        # mark start of else branch

    def exitIf(self, node):
        self.file.write(self.endLabel + ":" + "\n")

    def enterWhile(self, node):
        self.startLabel = self.getFreeLabel()
        self.file.write(self.startLabel + ":" + "\n")

    def enterWhileBranch(self, node):
        # Make sure expression is evaluated first
        self.endLabel = self.getFreeLabel()
        self.file.write("fjp " + self.endLabel + "\n")      # jump to end

    def exitWhile(self, node):
        self.file.write("ujp " + self.startLabel + "\n")    # end of while branch -> jump to start
        self.file.write(self.endLabel + ":" + "\n")
