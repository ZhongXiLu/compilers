
from ASTListener import ASTListener
from SymbolTable.SymbolTable import *
from SymbolTable.SymbolInfo import *
from AST import Expression, Function, Literals, Program, Statement, Variable
from SemanticValidator import SemanticValidator, getType


class CodeGenerator(ASTListener):

    def __init__(self, symbolTable, file="p_prog.p"):
        self.symbolTable = symbolTable
        self.nextFreeAddress = [5]      # stack = environment (5 reserved registers)
        self.labelId = 0

        # Temporary variables
        self.ifEndLabel = []            # temporary store label names to use for later (= stack)
        self.elseLabel = []
        self.whileStartLabel = []
        self.whileEndLabel = []
        self.skipMutable = False         # small hack to make sure mutables arent printed on lhs
        self.skipSubScript = False
        self.scanf = False
        self.printf = False
        self.skipFirst = False
        self.arrayIndex = False

        self.file = open(file, "w")


    def getFreeAddress(self):
        self.nextFreeAddress[-1] += 1
        return self.nextFreeAddress[-1] - 1

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
        self.file.write("mst 0\n")
        self.file.write("cup 0 main\n")
        self.file.write("hlt\n")

    def exitProgram(self, node):
        self.symbolTable.currentScope = self.symbolTable.currentScope.parent
        self.file.close()

    def enterCompound(self, node):
        self.symbolTable.currentScope = self.symbolTable.currentScope.getNextScope()
        self.nextFreeAddress.append(self.nextFreeAddress[-1])

    def exitCompound(self, node):
        self.symbolTable.currentScope = self.symbolTable.currentScope.parent
        self.nextFreeAddress.pop()

    def enterFunctionDef(self, node):
        self.symbolTable.currentScope = self.symbolTable.currentScope.getNextScope()
        self.nextFreeAddress.append(5)

        self.file.write(node.name + ":" + "\n")
        self.file.write("ssp " + str(len(node.params.params) + 5) + "\n")
        # Note: we dont have to set the extreme pointer, since we dont allow dynamic memory allocation
        # self.file.write("sep " + i + "\n")

        # Update the addresses of the parameters
        for param in node.params.params:
            if param.size is None:
                # only need one register
                self.symbolTable.getSymbol(param.name).address = self.getFreeAddress()
            else:
                self.symbolTable.getSymbol(param.name).address = self.getFreeAddress()
                self.nextFreeAddress[-1] += param.size

    def exitFunctionDef(self, node):
        self.symbolTable.currentScope = self.symbolTable.currentScope.parent
        self.nextFreeAddress.pop()

        # Check if the function is a void function, if so, create an explicit return instruction to mark the end
        if node.returns == "void":
            self.file.write("retp\n")

    def enterVarDeclInitialize(self, node):
        # Initialize variable with default value
        self.symbolTable.getSymbol(node.name).address = self.getFreeAddress()
        if self.getPType(self.symbolTable.getSymbol(node.name).type) == "c":
            # Check if we have to store a string, if so, allocate memory for it (one char = one address)
            if self.symbolTable.getSymbol(node.name).type == "char*":
                self.nextFreeAddress[-1] = self.symbolTable.getSymbol(node.name).address + len(node.expression.value)
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
            # TODO: recursion
            self.file.write("str " + self.getPType(symbol.type) + " 0 " + str(symbol.address) + "\n")

    def enterArrayInitialize(self, node):
        # Initialize array with default values
        freeAddress = self.getFreeAddress()
        self.symbolTable.getSymbol(node.name).address = freeAddress
        self.nextFreeAddress[-1] = freeAddress + int(node.size)

        for i in range(int(node.size)):
            if self.getPType(self.symbolTable.getSymbol(node.name).type) == "c":
                self.file.write("ldc c ' '\n")
            elif self.getPType(self.symbolTable.getSymbol(node.name).type) == "r":
                self.file.write("ldc r 0.0\n")
            else:
                self.file.write("ldc i 0\n")

    def exitArrayInitialize(self, node):
        symbol = self.symbolTable.getSymbol(node.name)
        for i in range(len(node.initialize.list)):
            # TODO: recursion
            self.file.write("str " + self.getPType(symbol.type) + " 0 " + str(symbol.address + int(node.size) - i - 1) + "\n")

    def enterMutable(self, node):
        if not self.skipMutable and not self.scanf:
            symbol = self.symbolTable.getSymbol(node.name)
            if type(symbol) is ArrayInfo:
                for i in range(int(symbol.size)):
                    if self.printf:
                        self.file.write("lod " + self.getPType(symbol.type) + " 0 " + str(symbol.address + int(symbol.size) - i - 1) + "\n")
                    else:
                        self.file.write("lod " + self.getPType(symbol.type) + " 0 " + str(symbol.address + i) + "\n")
            else:
                # self.file.write("ldo " + self.getPType(symbol.type) + " " + str(symbol.address) + "\n")
                self.file.write("lod " + self.getPType(symbol.type) + " 0 " + str(symbol.address) + "\n")
        else:
            if self.skipMutable:
                self.skipMutable = False

    def enterSubScript(self, node):
        # Load the start address of the array
        self.file.write("ldc a " + str(self.symbolTable.getSymbol(node.mutable.name).address) + "\n")
        self.skipMutable = True
        self.arrayIndex = True

    def exitSubScript(self, node):
        self.arrayIndex = False
        # expression (on the stack) is the index of the accessed array
        self.file.write("ixa " + str(1) + "\n")     # we only allow one dimensional arrays
        if not self.skipSubScript and not self.scanf:
            self.file.write("ind " + self.getPType(self.symbolTable.getSymbol(node.mutable.name).type) + "\n")
        else:
            self.skipSubScript = False

    def enterCall(self, node):
        if node.funcName == "scanf":
            self.scanf = True
        elif node.funcName == "printf":
            self.printf = True
            self.skipFirst = True
            string = node.args.pop(0)
            node.args.reverse()             # small hack to reverse the order of the arguments on the stack
            for index, arg in enumerate(node.args):
                # make sure the quotes arent put on stack and the string are reversed too
                if type(arg) == Literals.String:
                    arg.value = arg.value[1:-1]
                    arg.value = arg.value[::-1]
            node.args.insert(0, string)     # make sure the string stays at the first place
        else:
            self.file.write("mst 0\n")  # TODO: check for recursion

    def exitCall(self, node):
        if node.funcName == "scanf":
            self.scanf = False
            if node.args[0].value == "\"%c\"":
                self.file.write("in c\n")
            elif node.args[0].value == "\"%s\"":
                self.file.write("in c\n")     # TODO
            elif node.args[0].value == "\"%i\"":
                self.file.write("in i\n")
            elif node.args[0].value == "\"%d\"":
                self.file.write("in r\n")
            else:
                raise Exception(node.getPosition() + ": Only following type codes are supported: c, s, i, d")

            # Write scanned result to variable
            if type(node.args[1]) is Expression.Mutable:
                # self.skipMutable = True
                symbol = self.symbolTable.getSymbol(node.args[1].name)
                # TODO: recursion
                self.file.write("str " + self.getPType(symbol.type) + " 0 " + str(symbol.address) + "\n")
            elif type(node.args[1]) is Expression.SubScript:
                symbol = self.symbolTable.getSymbol(node.args[1].mutable.name)
                self.file.write("sto " + self.getPType(symbol.type) + "\n")
            else:
                raise Exception(node.getPosition() + ": Segmentation Fault")

        elif node.funcName == "printf":
            self.printf = False
            self.skipFirst = False

            string = node.args[0].value
            index = 1   # dont print the surrounding quotes
            paramCount = len(node.args)-1  # indicates at which param we are (note that the args are reversed)
            while index < len(string) - 1:
                if index != 0 and index != len(string)-1:
                    if string[index] == "%":
                        if string[index+1] == "c":
                            self.file.write("out c\n")

                        elif string[index+1] == "s":
                            if type(node.args[paramCount]) is Literals.String:
                                # print all characters of string (exclusive the quotes)
                                for i in range(len(node.args[paramCount].value)):
                                    self.file.write("out c\n")
                            else:
                                for i in range(int(self.symbolTable.getSymbol(node.args[paramCount].name).size)):
                                    self.file.write("out c\n")
                        elif string[index+1] == "i":
                            self.file.write("out i\n")
                        elif string[index+1] == "d":
                            self.file.write("out r\n")
                        else:
                            raise Exception(
                                node.getPosition() + ": Only following type codes are supported: c, s, i, d")
                        paramCount -= 1
                        index += 1
                    else:
                        self.file.write("ldc c '" + str(string[index]) + "'\n")
                        self.file.write("out c\n")
                index += 1

        else:
            self.file.write("cup " + str(len(node.args)) + " " + node.funcName + "\n")

    def enterInt(self, node):
        if not self.scanf or self.arrayIndex:
            self.file.write("ldc i " + str(node.value) + "\n")

    def enterDouble(self, node):
        if not self.scanf:
            self.file.write("ldc r " + str(node.value) + "\n")

    def enterString(self, node):
        if not self.scanf and not self.skipFirst:
            for char in node.value:
                self.file.write("ldc c '" + str(char) + "'\n")
        else:
            self.skipFirst = False

    def enterChar(self, node):
        if not self.scanf:
            self.file.write("ldc c " + str(node.value) + "\n")

    def enterAssign(self, node):
        if type(node.left) is Expression.Mutable:
            self.skipMutable = True
        else:
            self.skipSubScript = True

    def exitAssign(self, node):
        if type(node.left) is Expression.Mutable:
            symbol = self.symbolTable.getSymbol(node.left.name)
            # TODO: recursion
            self.file.write("str " + self.getPType(symbol.type) + " 0 " + str(symbol.address) + "\n")
        else:
            # note address of index is already on stack
            self.file.write("sto " + self.getPType(self.symbolTable.getSymbol(node.left.mutable.name).type) + "\n")

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
            self.ifEndLabel.append(self.getFreeLabel())
            self.file.write("fjp " + self.ifEndLabel[-1] + "\n")        # jump to end
        else:
            self.elseLabel.append(self.getFreeLabel())
            self.file.write("fjp " + self.elseLabel[-1] + "\n")         # jump to else branch

    def enterElseBranch(self, node):
        self.ifEndLabel.append(self.getFreeLabel())
        self.file.write("ujp " + self.ifEndLabel[-1] + "\n")            # end of if branch -> jump to end
        self.file.write(self.elseLabel.pop() + ":" + "\n")              # mark start of else branch

    def exitIf(self, node):
        self.file.write(self.ifEndLabel.pop() + ":" + "\n")

    def enterWhile(self, node):
        self.whileStartLabel.append(self.getFreeLabel())
        self.file.write(self.whileStartLabel[-1] + ":" + "\n")

    def enterWhileBranch(self, node):
        # Make sure expression is evaluated first
        self.whileEndLabel.append(self.getFreeLabel())
        self.file.write("fjp " + self.whileEndLabel[-1] + "\n")         # jump to end

    def exitWhile(self, node):
        self.file.write("ujp " + self.whileStartLabel.pop() + "\n")     # end of while branch -> jump to start
        self.file.write(self.whileEndLabel.pop() + ":" + "\n")

    def exitBreak(self, node):
        self.file.write("ujp " + self.whileEndLabel[-1] + "\n")     # jump to end

    def exitReturn(self, node):
        if node.expression is not None:
            # TODO: check for recursion
            self.file.write("str " + self.getPType(getType(node.expression, "", self.symbolTable)[0]) + " 0 0\n")
            self.file.write("retf\n")  # result in local stack
        else:
            self.file.write("retp\n")
