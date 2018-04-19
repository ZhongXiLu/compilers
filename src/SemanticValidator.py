
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
        print("enterVariableDecl")
        declList = node.declList
        for varDeclInit in declList.declInitializeList:
            # Check if new var already exists in current scope
            symbolInfo = self.symbolTable.getSymbolInCurrentScope(varDeclInit.name)
            if symbolInfo is None:
                if hasattr(varDeclInit, 'size'):
                    self.symbolTable.addSymbol(varDeclInit.name, ArrayInfo(node.type, varDeclInit.size))
                else:
                    self.symbolTable.addSymbol(varDeclInit.name, VarInfo(node.type))
                # if type(node) is Variable.VarDeclInitialize:
                #    self.symbolTable.addSymbol(varDeclInit.name, VarInfo(node.type))
                # else:
                #    self.symbolTable.addSymbol(varDeclInit.name, ArrayInfo(node.type, varDeclInit.size))
            else:
                self.errors.append(varDeclInit.getPosition() + ": Redefinition of '" + varDeclInit.name + "'")

    def enterVarDeclInitialize(self, node):
        print("enterVarDeclInitialize")
        symbolInfo=self.symbolTable.getSymbol(node.name)
        if(node.expression!=None):
            getTypeResult = getType(node.expression,symbolInfo.type,self.symbolTable)
            if (symbolInfo.type != getTypeResult[0] and getTypeResult[0] != "undefined input"):
                self.errors.append("Line "+ str(getTypeResult[1]) +" at "+ str(getTypeResult[2]) + ": Type mismatch: expected \"" + symbolInfo.type + "\" but found \"" + getTypeResult[0] + "\".")

    def enterCall(self, node):
        symbolInfo = self.symbolTable.getSymbol(node.funcName)
        if symbolInfo is None or type(symbolInfo) is not FunctionInfo:
            if node.funcName != "printf" and node.funcName != "scanf":
                self.errors.append(node.getPosition() + ": Undefined reference to '" + node.funcName + "'")
        else:
            if(len(node.args)==len(symbolInfo.paramTypes)):
                for i in range (0,len(symbolInfo.paramTypes)):
                    foundParamType= getType(node.args[i],symbolInfo.paramTypes[i],self.symbolTable)[0]
                    if(foundParamType!=symbolInfo.paramTypes[i]):
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

    def enterAssign(self, node):
        print("enterAssign")
        symbolInfo=None
        if(hasattr(node.left,"mutable")):
            symbolInfo = self.symbolTable.getSymbol(node.left.mutable.name)
            if(int(symbolInfo.size)<int(node.left.index._int)):
                self.errors.append("Line " + str(node.left.index.lineNr) + " at " + str(node.left.index.positionNr) + ": Index out of range! Max index: \"" + str(int(symbolInfo.size)-1) + "\" but found \"" +str(node.left.index._int) + "\".")
                return
        else:
            symbolInfo = self.symbolTable.getSymbol(node.left.name)
        getTypeResult =getType(node.right,symbolInfo.type,self.symbolTable)
        if (symbolInfo.type != getTypeResult[0] and getTypeResult[0]!="undefined input"):
            self.errors.append("Line "+ str(getTypeResult[1]) +" at "+ str(getTypeResult[2]) + ": Type mismatch: expected \"" + symbolInfo.type + "\" but found \"" + getTypeResult[0] + "\".")

def getType(node,expectedType,symbolTable):
    if(hasattr(node,"left")):
        assignee="assignee"
        if (hasattr(node.right, "name")):
            assignee = symbolTable.getSymbol(node.right.name)
        if(hasattr(node.right,"funcName")):
            assignee = symbolTable.getSymbol(node.right.funcName)
        if (assignee != None):
            assigneeType="AType"
            if(hasattr(assignee,"type")):
                assigneeType=assignee.type
            if(hasattr(assignee,"returnType")):
                assigneeType=assignee.returnType
            if(hasattr(node.right,"_int") or assigneeType=="short" or assigneeType=="int" or assigneeType=="signed" or assigneeType=="unsigned"):
                if(expectedType=="short" or expectedType=="int" or expectedType=="signed" or expectedType=="unsigned" or expectedType == "float" or expectedType == "double"):
                    return getType(node.left, expectedType,symbolTable)
                else:
                    return ["int",node.right.lineNr,node.right.positionNr]
            if (hasattr(node.right, "double") or assigneeType=="double" or assigneeType=="float"):
                if(expectedType == "float" or expectedType == "double"):
                    return getType(node.left, expectedType,symbolTable)
                else:
                    return ["double",node.right.lineNr,node.right.positionNr]
            if (hasattr(node.right, "string") or assigneeType=="string"):
                if(expectedType=="char"):
                    return getType(node.left, expectedType,symbolTable)
                else:
                    return ["string",node.right.lineNr,node.right.positionNr]
        else:
            return ["undefined input",node.right.lineNr,node.right.positionNr]
    else:
        if(hasattr(node,"_int")):
            if(expectedType=="short" or expectedType=="int" or expectedType=="signed" or expectedType=="unsigned" or expectedType == "float" or expectedType == "double"):
                return [expectedType,node.lineNr,node.positionNr]
            else:
                return ["int",node.lineNr,node.positionNr]
        if(hasattr(node,"double")):
            if(expectedType == "float" or expectedType == "double"):
                return [expectedType,node.lineNr,node.positionNr]
            else:
                return ["double",node.lineNr,node.positionNr]
        if(hasattr(node,"string")):
            if(expectedType=="char"):
                return [expectedType,node.lineNr,node.positionNr]
            else:
                return ["string",node.lineNr,node.positionNr]
        if(hasattr(node,"name")):
            assigneeType = symbolTable.getSymbol(node.name)
            if(assigneeType!=None):
                return [assigneeType.type,node.lineNr,node.positionNr]
            else:
                return ["undefined variable",node.right.lineNr,node.right.positionNr]
        if(hasattr(node,"funcName")):
            functionType = symbolTable.getSymbol(node.funcName)
            if(functionType!=None):
                return [functionType.returnType,node.lineNr,node.positionNr]
            else:
                return["undefined input",node.lineNr,node.positionNr]