
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
                if type(node) is Variable.ArrayInitialize:
                    self.symbolTable.addSymbol(varDeclInit.name, ArrayInfo(node.type, varDeclInit.size))
                else:
                    self.symbolTable.addSymbol(varDeclInit.name, VarInfo(node.type))
            else:
                self.errors.append(varDeclInit.getPosition() + ": Redefinition of '" + varDeclInit.name + "'")

    def enterVarDeclInitialize(self, node):
        symbolInfo=self.symbolTable.getSymbol(node.name)
        if node.expression is not None:
            getTypeResult = getType(node.expression,symbolInfo.type, self.symbolTable)
            if symbolInfo.type != getTypeResult[0] and getTypeResult[0] != "undefined input":
                self.errors.append("Line "+ str(getTypeResult[1]) +" at "+ str(getTypeResult[2]) + ": Type mismatch: expected \"" + symbolInfo.type + "\" but found \"" + getTypeResult[0] + "\".")

    def enterCall(self, node):
        symbolInfo = self.symbolTable.getSymbol(node.funcName)
        if symbolInfo is None or type(symbolInfo) is not FunctionInfo:
            if node.funcName != "printf" and node.funcName != "scanf":
                self.errors.append(node.getPosition() + ": Undefined reference to '" + node.funcName + "'")
        else:
            if len(node.args) == len(symbolInfo.paramTypes):
                for i in range (0, len(symbolInfo.paramTypes)):
                    foundParamType = getType(node.args[i],symbolInfo.paramTypes[i],self.symbolTable)[0]
                    if foundParamType != symbolInfo.paramTypes[i]:
                        self.errors.append(node.getPosition() + ": Wrong parameter type! Expected: \"" + symbolInfo.paramTypes[i] + "\" found \""+foundParamType+"\"")
            else:self.errors.append(node.getPosition() + ": Wrong amount of parameters! Expected: " + str(len(symbolInfo.paramTypes)) + " found " + str(len(node.args)))

    def enterMutable(self, node):
        symbolInfo = self.symbolTable.getSymbol(node.name)
        if symbolInfo is None or (type(symbolInfo) is not VarInfo and type(symbolInfo) is not ArrayInfo):
            self.errors.append(node.getPosition() + ": Undefined reference to '" + node.name + "'")

    def enterSubScript(self, node):
        symbolInfo = self.symbolTable.getSymbol(node.mutable.name)
        if symbolInfo is None or type(symbolInfo) is not ArrayInfo:
            self.errors.append(node.getPosition() + ": Subscripted value '" + node.mutable.name + "' is not an array")

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

    def enterAssign(self, node):
        symbolInfo = None
        if type(node.left) is Expression.SubScript:
            symbolInfo = self.symbolTable.getSymbol(node.left.mutable.name)
            if int(symbolInfo.size) < int(node.left.index._int):
                self.errors.append(node.left.index.getPosition() + ": Index out of range! Max index: \"" + str(int(symbolInfo.size)-1) + "\" but found \"" +str(node.left.index._int) + "\".")
                return
        else:
            symbolInfo = self.symbolTable.getSymbol(node.left.name)
            getTypeResult = getType(node.right,symbolInfo.type,self.symbolTable)
            if symbolInfo.type != getTypeResult[0] and getTypeResult[0] != "undefined input":
                self.errors.append(getTypeResult[1] + ": Type mismatch: expected \"" + symbolInfo.type + "\" but found \"" + getTypeResult[0] + "\".")


def getType(expression,expectedType,symbolTable):

    if type(expression) is Expression.BinOp:
        assignee = "assignee"
        if type(expression.right) is Expression.Mutable:
            assignee = symbolTable.getSymbol(expression.right.name)
        if type(expression.right) is Expression.Call:
            assignee = symbolTable.getSymbol(expression.right.funcName)
        if assignee is not None:    # Opmerking: is toch altijd "not None"?
            assigneeType = "AType"
            if hasattr(assignee, "type"):
                assigneeType = assignee.type
            if hasattr(assignee, "returnType"):
                assigneeType = assignee.returnType
            if type(expression.right) is Literals.Int or assigneeType == "short" or assigneeType == "int" \
                    or assigneeType == "signed" or assigneeType == "unsigned":
                if expectedType == "short" or expectedType == "int" or expectedType == "signed"\
                        or expectedType == "unsigned" or expectedType == "float" or expectedType == "double":
                    return getType(expression.left, expectedType,symbolTable)
                else:
                    return ["int", expression.right.getPosition()]
            if type(expression.right) is Literals.Double or assigneeType == "double" or assigneeType == "float":
                if expectedType == "float" or expectedType == "double":
                    return getType(expression.left, expectedType, symbolTable)
                else:
                    return ["double", expression.right.getPosition()]
            if type(expression.right) is Literals.String or assigneeType == "string":
                if expectedType == "char":
                    return getType(expression.left, expectedType, symbolTable)
                else:
                    return ["string", expression.right.getPosition()]
        else:
            return ["undefined input", expression.right.getPosition()]

    elif type(expression) is Expression.Mutable:
        assigneeType = symbolTable.getSymbol(expression.name)
        if assigneeType is not None:
            return [assigneeType.type, expression.getPosition()]
        else:
            return ["undefined variable", expression.right.getPosition()]
    elif type(expression) is Expression.Call:
        functionType = symbolTable.getSymbol(expression.funcName)
        if functionType is not None:
            return [functionType.returnType, expression.getPosition()]
        else:
            return ["undefined input", expression.getPosition()]

    else:
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
                return ["string", expression.lineNr.getPosition()]