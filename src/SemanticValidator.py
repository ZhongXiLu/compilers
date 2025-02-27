
from ASTListener import ASTListener
from SymbolTable.SymbolTable import *
from SymbolTable.SymbolInfo import *
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
                if type(varDeclInit) is Variable.ArrayInitialize:
                    self.symbolTable.addSymbol(varDeclInit.name, ArrayInfo(node.type, varDeclInit.size))
                else:
                    self.symbolTable.addSymbol(varDeclInit.name, VarInfo(node.type))
            else:
                self.errors.append(varDeclInit.getPosition() + ": Redefinition of '" + varDeclInit.name + "'")

    def enterVarDeclInitialize(self, node):
        symbolInfo = self.symbolTable.getSymbol(node.name)
        if node.expression is not None:
            # if (node.expression is Expression.BinOp and (symbolInfo.type == "char" and not hasattr(symbolInfo,type))):
            #     self.errors.append(
            #         node.getPosition() + ": Type mismatch: expected '" + symbolInfo.type + "' but found 'BinOp'")
            # else:
            #     getTypeResult = getType(node.right, symbolInfo.type, self.symbolTable)
            #     if symbolInfo.type != getTypeResult[0] and getTypeResult[0] != "undefined input":
            #         self.errors.append(getTypeResult[1] + ": Type mismatch: expected '" + symbolInfo.type + "' but found '" +getTypeResult[0] + "'")
            if (isinstance(node.expression,Expression.BinOp)and (symbolInfo.type == "char" and not hasattr(symbolInfo,"size"))):
                self.errors.append(node.getPosition() + ": Type mismatch: expected '" + symbolInfo.type + "' but found 'BinOp'")
            else:
                getTypeResult = getType(node.expression, symbolInfo.type, self.symbolTable)
                if symbolInfo.type != getTypeResult[0] and getTypeResult[0] != "undefined input":
                    self.errors.append(getTypeResult[1] + ": Type mismatch for '" + node.name + "': expected '" + symbolInfo.type + "' but found '" +getTypeResult[0] + "'")

    def enterCall(self, node):
        symbolInfo = self.symbolTable.getSymbol(node.funcName)
        if symbolInfo is None or type(symbolInfo) is not FunctionInfo:
            if node.funcName == "printf" or node.funcName == "scanf":
                if len(node.args) > 0:
                    paramType = getType(node.args[0], "string", self.symbolTable)
                    if paramType[0] != "string" and paramType[0] != "char*":
                        self.errors.append(paramType[1] + ": Wrong parameter type for '" + node.funcName + "'! Expected: 'char*' found '" + paramType[0] + "'")
                else:
                    self.errors.append(node.getPosition() + ": Wrong amount of parameters for '" + node.funcName + "'! Expected at least one argument")

            else:
                self.errors.append(node.getPosition() + ": Undefined reference to '" + node.funcName + "'")
        else:
            symbolInfo.used = True
            if symbolInfo.isDecl:
                self.errors.append(node.getPosition() + ": Undefined reference to '" + node.funcName + "'")
            else:
                if len(node.args) == len(symbolInfo.paramTypes):
                    for i in range (0, len(symbolInfo.paramTypes)):
                        foundParamType = getType(node.args[i], symbolInfo.paramTypes[i],self.symbolTable)[0]
                        if foundParamType != symbolInfo.paramTypes[i]:
                            self.errors.append(node.getPosition() + ": Wrong parameter type for '" + node.funcName + "'! Expected: '" + symbolInfo.paramTypes[i] + "' found '" + foundParamType + "'")
                else:
                    self.errors.append(node.getPosition() + ": Wrong amount of parameters for '" + node.funcName + "'! Expected: " + str(len(symbolInfo.paramTypes)) + " found " + str(len(node.args)))

    def enterMutable(self, node):
        symbolInfo = self.symbolTable.getSymbol(node.name)
        if symbolInfo is None or (type(symbolInfo) is not VarInfo and type(symbolInfo) is not ArrayInfo):
            self.errors.append(node.getPosition() + ": Undefined reference to '" + node.name + "'")
        else:
            symbolInfo.used = True

    def enterSubScript(self, node):
        symbolInfo = self.symbolTable.getSymbol(node.mutable.name)
        if symbolInfo is None or type(symbolInfo) is not ArrayInfo:
            self.errors.append(node.getPosition() + ": Subscripted value '" + node.mutable.name + "' is not an array")
        else:
            symbolInfo.used = True
            # if int(symbolInfo.size) < int(node.index._int):
            #     self.errors.append(node.index.getPosition() + ": Index out of range for '" + node.mutable.name + "'! Max index: '" + str(
            #         int(symbolInfo.size) - 1) + "' but found '" + str(node.index._int) + "'")

    def enterFunctionDef(self, node):
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

        elif type(symbolInfo) is FunctionInfo and symbolInfo.isDecl:
            # Previous declaration => check if definition matches declaration
            if node.returns != symbolInfo.type:
                self.errors.append(node.getPosition() + ": Wrong return type for '" + node.name + "'! Expected: '" + symbolInfo.type + "' found '" + node.returns + "'")

            params = node.params
            paramTypes = []
            if len(params.params) == len(symbolInfo.paramTypes):
                for i in range (0, len(symbolInfo.paramTypes)):
                    if params.params[i].type != symbolInfo.paramTypes[i]:
                        self.errors.append(params.params[i].getPosition() + ": Wrong parameter type for '" + node.name + "'! Expected: '" + symbolInfo.paramTypes[i] + "' found '" + params.params[i].type + "'")
                    paramTypes.append(params.params[i].type)
                    self.symbolTable.addSymbol(params.params[i].name, VarInfo(params.params[i].type))
            else:
                self.errors.append(node.getPosition() + ": Wrong amount of parameters for '" + node.name + "'! Expected: " + str(len(symbolInfo.paramTypes)) + " found " + str(len(params.params)))

            self.symbolTable.addSymbol(node.name, FunctionInfo(node.returns, paramTypes))
            self.symbolTable.newScope()

        else:
            self.errors.append(node.getPosition() + ": Redefinition of '" + node.name + "'")

    def exitFunctionDef(self, node):
        self.symbolTable.endScope()

    def enterFunctionDecl(self, node):
        # Check if new function already exists
        symbolInfo = self.symbolTable.getSymbol(node.name)
        if symbolInfo is None:
            params = node.params
            paramTypes = []
            for param in params.params:
                paramTypes.append(param.type)
            self.symbolTable.addSymbol(node.name, FunctionInfo(node.returns, paramTypes, isDecl=True))
        else:
            self.errors.append(node.getPosition() + ": Redefinition of '" + node.name + "'")

    def enterAssign(self, node):
        symbolInfo = None
        if type(node.left) is Expression.SubScript:
            symbolInfo = self.symbolTable.getSymbol(node.left.mutable.name)
        else:
            symbolInfo = self.symbolTable.getSymbol(node.left.name)
        if symbolInfo is not None:
            if (isinstance(node.right,Expression.BinOp) and (symbolInfo.type == "char" and not hasattr(symbolInfo,"size"))):
                self.errors.append(node.getPosition() + ": Type mismatch: expected '" + symbolInfo.type + "' but found 'BinOp'")
            else:
                getTypeResult = getType(node.right, symbolInfo.type, self.symbolTable)
                if((symbolInfo.type == "float" or symbolInfo.type=="double") and (getTypeResult[0]!="float" and getTypeResult[0]!="double")):
                    self.errors.append(getTypeResult[1] + ": Type mismatch: expected '" + symbolInfo.type + "' but found '" +getTypeResult[0] + "'")
                elif ((symbolInfo.type=="int" or symbolInfo.type=="long" or symbolInfo.type=="signed" or symbolInfo.type=="unsigned")and(getTypeResult[0]!="int" and getTypeResult[0]!="long" and getTypeResult[0]!="signed" and getTypeResult[0]!="unsigned")):
                    self.errors.append(getTypeResult[1] + ": Type mismatch: expected '" + symbolInfo.type + "' but found '" +getTypeResult[0] + "'")

    def enterBinOp(self, node):
        foundMismatch=False
        if type(node.left) is not Expression.BinOp:
            leftType = getType(node.left,"",self.symbolTable)[0]
        else:
           leftTypeResult = checkBinOp(node.left,self.symbolTable)

           if (leftTypeResult[0] == "string" or leftTypeResult[0] == "char"):
               if (leftTypeResult[1] == "string" or leftTypeResult[1] == "char"):
                   leftType = leftTypeResult[0]
               else:
                   foundMismatch = True
                   error = leftTypeResult[2].getPosition() + ": type mismatch! Cannot compare '" + leftTypeResult[
                       0] + "' with '" + leftTypeResult[1] + "'"
                   if error not in self.errors:
                       self.errors.append(error)

           else:
               if (leftTypeResult[1] == "string" or leftTypeResult[1] == "char"):
                   foundMismatch = True
                   error = leftTypeResult[2].getPosition() + ": type mismatch! Cannot compare '" + leftTypeResult[
                       0] + "' with '" + leftTypeResult[1] + "'"
                   if error not in self.errors:
                       self.errors.append(error)

               else:
                   leftType = leftTypeResult[0]
        if type(node.right)is not Expression.BinOp:
            rightType = getType(node.right,"",self.symbolTable)[0]
        else:
            rightTypeResult = checkBinOp(node.right,self.symbolTable)
            if (rightTypeResult[0] == "string" or rightTypeResult[0] == "char"):
                if (rightTypeResult[1] == "string" or rightTypeResult[1] == "char"):
                    rightType = rightTypeResult[0]
                else:
                    foundMismatch = True
                    error = rightTypeResult[2].getPosition() + ": type mismatch! Cannot compare '" + rightTypeResult[
                        0] + "' with '" + rightTypeResult[1] + "'"
                    if error not in self.errors:
                        self.errors.append(error)

            else:
                if (rightTypeResult[1] == "string" or rightTypeResult[1] == "char"):
                    foundMismatch = True
                    error = rightTypeResult[2].getPosition() + ": type mismatch! Cannot compare '" + rightTypeResult[
                        0] + "' with '" + rightTypeResult[1] + "'"
                    if error not in self.errors:
                        self.errors.append(error)

                else:
                    rightType = rightTypeResult[0]

        if not foundMismatch:
            if(leftType == "string" or leftType == "char"):
                if(rightType!="string" and rightType!="char"):
                    error = node.getPosition() + ": type mismatch! Cannot compare '" + leftType + "' with '" + rightType + "'"
                    if error not in self.errors:
                        self.errors.append(error)
            else:
                if(rightType=="string" or rightType=="char"):
                    error = node.getPosition() + ": type mismatch! Cannot compare '" + leftType + "' with '" +rightType+ "'"
                    if error not in self.errors:
                        self.errors.append(error)


def getType(expression,expectedType,symbolTable):
    if type(expression) is Expression.BinOp:
        assignee = "assignee"
        if type(expression.right) is Expression.BinOp:
            if expression.right.operator.value == "<" or expression.right.operator.value == ">" or expression.right.operator.value == "==":
                return ["int", expression.right.getPosition()]
            else:
                childResult = checkBinOp(expression.right, symbolTable)
                return [childResult[1], childResult[2].getPosition()]
        if type(expression.right) is Expression.Mutable:
            assignee = symbolTable.getSymbol(expression.right.name)
        if type(expression.right) is Expression.Call:
            assignee = symbolTable.getSymbol(expression.right.funcName)
        if type(expression.right) is Expression.SubScript:
            assignee = symbolTable.getSymbol(expression.right.mutable.name)
        if assignee is not None:    # Opmerking: is toch altijd "not None"?
            assigneeType = "AType"
            if hasattr(assignee, "type"):
                assigneeType = assignee.type
            if type(expression.right) is Literals.Int or assigneeType == "short" or assigneeType == "int" \
                    or assigneeType == "signed" or assigneeType == "unsigned":
                if expectedType == "short" or expectedType == "int" or expectedType == "signed"\
                        or expectedType == "unsigned" or expectedType == "float" or expectedType == "double":
                    return getType(expression.left, expectedType, symbolTable)
                else:
                    return ["int", expression.right.getPosition()]
            if type(expression.right) is Literals.Double or assigneeType == "double" or assigneeType == "float":
                if expectedType == "float" or expectedType == "double":
                    return getType(expression.left, expectedType, symbolTable)
                else:
                    return ["double", expression.right.getPosition()]
            if type(expression.right) is Literals.String or assigneeType == "string" or Literals.Char or assigneeType=="char":
                if expectedType == "char":
                    return getType(expression.left, expectedType, symbolTable)
                else:
                    return ["string", expression.right.getPosition()]

        else:
            return ["undefined input", expression.right.getPosition()]

    foundType = None
    if type(expression) is Expression.Mutable:
        found = symbolTable.getSymbol(expression.name)
        if found is not None:
            foundType = found.type
        else:
            foundType = "undefined input"
    if type(expression) is Expression.Call:
        found = symbolTable.getSymbol(expression.funcName)
        if found is not None:
            foundType = found.type
        else:
            foundType = "undefined input"
    if type(expression) is Expression.SubScript:
        found = symbolTable.getSymbol(expression.mutable.name)
        if found is not None:
            foundType = found.type
        else:
            foundType = "undefined input"

    if foundType is not None:
        if foundType!="undefined input":
            if foundType == "short" or foundType == "int" or foundType == "signed" or foundType == "unsigned":
                if expectedType == "short" or expectedType == "int" or expectedType == "signed" or expectedType == "unsigned" or expectedType == "float" or expectedType == "double":
                    return [expectedType,expression.getPosition()]
                else:
                    return [foundType, expression.getPosition()]
            if foundType == "double" or foundType == "float":
                if expectedType == "float" or expectedType == "double":
                    return [expectedType, expression.getPosition()]
                else:
                    return [foundType, expression.getPosition()]
            if foundType == "string":
                if expectedType == "char" or expectedType=="string":
                    return [expectedType, expression.getPosition()]
                else:
                    return [foundType, expression.getPosition()]
            if foundType =="char":
                if expectedType == "char":
                    return [expectedType, expression.getPosition()]
                else:
                    return [foundType, expression.getPosition()]
        else:
            return ["undefined input", expression.getPosition()]

    # Literals
    if type(expression) is Literals.Int:
        if expectedType == "short" or expectedType == "int" or expectedType == "signed" or expectedType == "unsigned"\
                or expectedType == "float" or expectedType == "double":
            return [expectedType, expression.getPosition()]
        else:
            return ["int", expression.getPosition()]
    if type(expression) is Literals.Double:
        if expectedType == "float" or expectedType == "double":
            return [expectedType, expression.getPosition()]
        else:
            return ["double", expression.getPosition()]
    if type(expression) is Literals.String:
        if expectedType == "char":
            return [expectedType, expression.getPosition()]
        else:
            return ["string", expression.getPosition()]
    if type(expression) is Literals.Char:
        if expectedType == "char":
            return [expectedType, expression.getPosition()]
        else:
            return ["char", expression.getPosition()]


def checkBinOp(expression,symbolTable):
    if type(expression.left) is not Expression.BinOp:
        leftType = getType(expression.left, "", symbolTable)[0]
    else:
        leftTypeResult = checkBinOp(expression.left, symbolTable)
        if (leftTypeResult[0] == "string" or leftTypeResult[0] == "char"):
            if (leftTypeResult[1] == "string" or leftTypeResult[1] == "char"):
                leftType = leftTypeResult[0]
            else:
                return [leftTypeResult[0], leftTypeResult[1], leftTypeResult[2]]
        else:
            if (leftTypeResult[1] == "string" or leftTypeResult[1] == "char"):
                return [leftTypeResult[0], leftTypeResult[1], leftTypeResult[2]]
            else:
                leftType = leftTypeResult[0]
    if type(expression.right) is not Expression.BinOp:
        rightType = getType(expression.right, "", symbolTable)[0]
    else:
        rightTypeResult = checkBinOp(expression.right, symbolTable)
        if (rightTypeResult[0] == "string" or rightTypeResult[0] == "char"):
            if (rightTypeResult[1] == "string" or rightTypeResult[1] == "char"):
                rightType = rightTypeResult[0]
            else:
                return [rightTypeResult[0], rightTypeResult[1], rightTypeResult[2]]
        else:
            if (rightTypeResult[1] == "string" or rightTypeResult[1] == "char"):
                return [rightTypeResult[0], rightTypeResult[1], rightTypeResult[2]]
            else:
                rightType = rightTypeResult[0]
    return[leftType,rightType,expression]
