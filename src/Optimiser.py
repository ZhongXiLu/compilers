
from ASTListener import ASTListener
from SymbolTable.SymbolTable import *
from AST import Expression, Function, Literals, Program, Statement, Variable
import sys

class Optimiser(ASTListener):

    def __init__(self, symbolTable):
        self.symbolTable = symbolTable
        self.warnings = []

    def enterProgram(self, node):
        self.symbolTable.reset()
        self.symbolTable.currentScope = self.symbolTable.currentScope.getNextScope()

    def exitProgram(self, node):
        # Check for unused functions
        i = 0
        while i < len(node.declarationList.declarations):
            if type(node.declarationList.declarations[i]) is Function.FunctionDef or \
                    type(node.declarationList.declarations[i]) is Function.FunctionDecl:
                # Note: main function is exception
                if node.declarationList.declarations[i].name != "main" and \
                        not self.symbolTable.getSymbol(node.declarationList.declarations[i].name).used:
                    self.warnings.append(node.getPosition() + ": Unused function '" + node.declarationList.declarations[i].name + "'")
                    del node.declarationList.declarations[i]
                    del self.symbolTable.currentScope.children[i]   # also delete the scope
                    i -= 1
            i += 1

        self.symbolTable.currentScope = self.symbolTable.currentScope.parent

    def returnInCompund(self, node):
        # Check for unreachable code
        for i in range(len(node.statements)):
            if type(node.statements[i]) is Statement.Return:
                if i < len(node.statements)-1:
                    self.warnings.append(node.getPosition() + ": Unreachable code after return")
                del node.statements[i + 1:]
                return True

            # Check if there's a return in the compound state
            elif type(node.statements[i]) is Statement.Compound:
                if self.returnInCompund(node.statements[i]):
                    if i < len(node.statements) - 1:
                        self.warnings.append(node.getPosition() + ": Unreachable code after return")
                    del node.statements[i + 1:]
                    return True

            # Check if there's a return in both the if and else branch
            elif type(node.statements[i]) is Statement.If:
                if node.statements[i].elseBody is not None:
                    returns = 0
                    if type(node.statements[i].body) is Statement.Return:
                        returns += 1
                    elif self.returnInCompund(node.statements[i].body):
                        returns += 1
                    if type(node.statements[i].elseBody) is Statement.Return:
                        returns += 1
                    elif self.returnInCompund(node.statements[i].elseBody):
                        returns += 1

                    if returns == 2:
                        if i < len(node.statements) - 1:
                            self.warnings.append(node.getPosition() + ": Unreachable code after return")
                        del node.statements[i + 1:]
                        return True

        return False

    def enterCompound(self, node):
        self.symbolTable.currentScope = self.symbolTable.currentScope.getNextScope()

        self.returnInCompund(node)

    def exitCompound(self, node):
        i = 0
        while i < len(node.localDecls):
            # Check if there are still variable initialisers left
            if not node.localDecls[i].declList.declInitializeList:
                del node.localDecls[i]
                i -= 1
            i += 1

        self.symbolTable.currentScope = self.symbolTable.currentScope.parent

    def enterWhile(self, node):

        # Check for unreachable code
        if type(node.body) is Statement.Compound:
            for i in range(len(node.body.statements)):
                if type(node.body.statements[i]) is Statement.Break:
                    self.warnings.append(node.getPosition() + ": Unreachable code after break")
                    del node.body.statements[i + 1:]
                    break
        # Still need to check for break's inside other statements..., no easy way to do it...

    def enterFunctionDef(self, node):
        self.symbolTable.currentScope = self.symbolTable.currentScope.getNextScope()

    def exitFunctionDef(self, node):
        self.symbolTable.currentScope = self.symbolTable.currentScope.parent

    def enterVarDeclList(self, node):
        # Check for unused variables
        i = 0
        while i < len(node.declInitializeList):
            if type(node.declInitializeList[i]) is Variable.VarDeclInitialize or \
                    type(node.declInitializeList[i]) is Variable.ArrayInitialize:
                if not self.symbolTable.getSymbol(node.declInitializeList[i].name).used:
                    self.warnings.append(node.getPosition() + ": Unused variable '" + node.declInitializeList[i].name + "'")
                    del node.declInitializeList[i]
                    i -= 1
            i += 1

    def enterCall(self, node):
        if(node.funcName!="printf" and node.funcName!="scanf"):
            funcInfo = self.symbolTable.getSymbol(node.funcName)
            newArguments = [None] * len(node.args)
            for i in range (0,len(node.args)):
                newArguments[i] = self.constantFolding(funcInfo.paramTypes[i],node.args[i])
                newArguments[i] = self.eraseNullSequences(node.args[i])
            node.args=newArguments

    def enterSubScript(self, node):
        node.index = self.constantFolding(self.symbolTable.getSymbol(node.mutable.name).type,node.index)
        node.index = self.eraseNullSequences(node.index)

    def enterAssign(self, node):
        if(isinstance(node.right,Expression.BinOp)):
            node.right = self.constantFolding(self.symbolTable.getSymbol(node.left.name).type,node.right)
            node.right = self.eraseNullSequences(node.right)

    def enterVarDeclInitialize(self, node):
        if (isinstance(node.expression,Expression.BinOp)):
            node.expression=self.constantFolding(self.symbolTable.getSymbol(node.name).type,node.expression)
            node.expression=self.eraseNullSequences(node.expression)

    def constantFolding(self,basicType,expression):
        if(isinstance(expression,Expression.BinOp)):
            if (basicType=="char"):
                if (isinstance(expression.left,Expression.BinOp)):
                    leftPart = self.constantFolding(basicType,expression.left)
                    if (isinstance(expression.right, Literals.String) or isinstance(expression.right,Literals.Char) or isinstance(expression.right, Literals.Int) or isinstance(expression.right, Literals.Double)):
                        if (isinstance(leftPart, Expression.BinOp)):
                            if (isinstance(leftPart.right, Literals.String) or isinstance(leftPart.right,Literals.Char) or isinstance(leftPart.right, Literals.Int) or isinstance(leftPart.right, Literals.Double)):
                                rightPart = Literals.String(leftPart.right.lineNr,leftPart.right.positionNr,leftPart.right.value[0:len(leftPart.right.value)-1]+ expression.right.value[1:len(expression.right.value)])
                                return Expression.BinOp(expression.lineNr,expression.positionNr,expression.operator,leftPart.left,rightPart)
                            else:
                                expression.left = leftPart
                                return expression
                        else:
                            return Literals.String(expression.lineNr, expression.positionNr,leftPart.value[0:len(leftPart.value) - 1] + expression.right.value[1:len(expression.right.value)])
                    else:
                        expression.left=leftPart
                        return expression
                else:
                    if((isinstance(expression.left, Literals.String) or isinstance(expression.left, Literals.Char) or isinstance(expression.left, Literals.Int) or isinstance(expression.left, Literals.Double))and(isinstance(expression.right, Literals.String) or isinstance(expression.right, Literals.Char) or isinstance(expression.right, Literals.Int) or isinstance(expression.right, Literals.Double))):
                        return Literals.String(expression.lineNr,expression.positionNr,expression.left.value[0:len(expression.left.value)-1]+ expression.right.value[1:len(expression.right.value)])
                    else:
                        return expression
            elif(basicType == "int" or basicType == "signed" or basicType=="unsigned" or basicType=="long"):
                if (isinstance(expression.left,Expression.BinOp)):
                    leftPart = self.constantFolding(basicType,expression.left)
                    if (isinstance(expression.right, Literals.Int)):
                        if (isinstance(leftPart, Expression.BinOp)):
                            if(leftPart.operator.value=="+" or leftPart.operator.value=="-"):
                                if (isinstance(leftPart.right, Literals.Int)):
                                    if (expression.operator.value == "+"):
                                        newValue = str(int(leftPart.right.value) + int(expression.right.value))
                                    elif (expression.operator.value == "-"):
                                        newValue = str(int(leftPart.right.value) - int(expression.right.value))
                                    elif (expression.operator.value == "*"):
                                        newValue = str(int(int(leftPart.right.value) * int(expression.right.value)))
                                    else:
                                        newValue = str(int(int(leftPart.right.value) / int(expression.right.value)))
                                    rightPart = Literals.Int(leftPart.right.lineNr,leftPart.right.positionNr,newValue)
                                    return Expression.BinOp(expression.lineNr,expression.positionNr,expression.operator,leftPart.left,rightPart)
                                else:
                                    expression.left = leftPart
                                    return expression
                            else:
                                expression.left = leftPart
                                return expression
                        else:
                            if (expression.operator.value == "+"):
                                newValue = str(int(leftPart.value) + int(expression.right.value))
                            elif (expression.operator.value == "-"):
                                newValue = str(int(leftPart.value) - int(expression.right.value))
                            elif (expression.operator.value == "*"):
                                newValue = str(int(int(leftPart.value) * int(expression.right.value)))
                            else:
                                newValue = str(int(int(leftPart.value) / int(expression.right.value)))
                            return Literals.Int(expression.lineNr, expression.positionNr,newValue)
                    elif(isinstance(expression.right,Expression.BinOp)):
                        rightPart=self.constantFolding(basicType,expression.right)
                        if(isinstance(rightPart,Literals.Int)):
                            if (isinstance(leftPart, Expression.BinOp)):
                                if (isinstance(leftPart.right, Literals.Int)):
                                    if (expression.operator.value == "+"):
                                        newValue = str(int(leftPart.right.value) + int(rightPart.value))
                                    elif (expression.operator.value == "-"):
                                        newValue = str(int(leftPart.right.value) - int(rightPart.value))
                                    elif (expression.operator.value == "*"):
                                        newValue = str(int(int(leftPart.right.value) * int(rightPart.value)))
                                    else:
                                        newValue = str(int(int(leftPart.right.value) / int(rightPart.value)))
                                    rightPart = Literals.Int(leftPart.right.lineNr, leftPart.right.positionNr, newValue)
                                    return Expression.BinOp(expression.lineNr, expression.positionNr, expression.operator,leftPart.left, rightPart)
                                else:
                                    expression.left = leftPart
                                    expression.right = rightPart
                                    return expression
                            else:
                                if (expression.operator.value == "+"):
                                    newValue = str(int(leftPart.value) + int(rightPart.value))
                                elif (expression.operator.value == "-"):
                                    newValue = str(int(leftPart.value) - int(rightPart.value))
                                elif (expression.operator.value == "*"):
                                    newValue = str(int(int(leftPart.value) * int(rightPart.value)))
                                else:
                                    newValue = str(int(int(leftPart.value) / int(rightPart.value)))
                                return Literals.Int(expression.lineNr, expression.positionNr, newValue)
                        else:
                            expression.left=leftPart
                            expression.right=rightPart
                            return expression
                    else:
                        expression.left=leftPart
                        return expression
                else:
                    if(isinstance(expression.left, Literals.Int)):
                        if(isinstance(expression.right, Literals.Int)):
                            if(expression.operator.value=="+"):
                                newValue = str(int(expression.left.value) + int(expression.right.value))
                            elif(expression.operator.value=="-"):
                                newValue = str(int(expression.left.value) - int(expression.right.value))
                            elif(expression.operator.value=="*"):
                                newValue = str(int(int(expression.left.value) * int(expression.right.value)))
                            else:
                                newValue = str(int(int(expression.left.value) / int(expression.right.value)))
                            return Literals.Int(expression.lineNr,expression.positionNr,newValue)
                        elif(isinstance(expression.right,Expression.BinOp)):
                            rightPart=self.constantFolding(basicType,expression.right)
                            if(isinstance(rightPart,Literals.Int)):
                                if (expression.operator.value == "+"):
                                    newValue = str(int(expression.left.value) + int(rightPart.value))
                                elif (expression.operator.value == "-"):
                                    newValue = str(int(expression.left.value) - int(rightPart.value))
                                elif (expression.operator.value == "*"):
                                    newValue = str(int(int(expression.left.value) * int(rightPart.value)))
                                else:
                                    newValue = str(int(int(expression.left.value) / int(rightPart.value)))
                                return Literals.Int(expression.lineNr, expression.positionNr, newValue)
                            else:
                                expression.right=rightPart
                                return expression
                        else:
                            return expression
                    else:
                        if(isinstance(expression.right,Expression.BinOp)):
                            expression.right = self.constantFolding(basicType,expression.right)
                        return expression
            else:
                if (isinstance(expression.left,Expression.BinOp)):
                    leftPart = self.constantFolding(basicType,expression.left)
                    if (isinstance(expression.right, Literals.Double)):
                        if (isinstance(leftPart, Expression.BinOp)):
                            if (isinstance(leftPart.right, Literals.Double)):
                                if (expression.operator.value == "+"):
                                    newValue = str(float(leftPart.right.value) + float(expression.right.value))
                                elif (expression.operator.value == "-"):
                                    newValue = str(float(leftPart.right.value) - float(expression.right.value))
                                elif (expression.operator.value == "*"):
                                    newValue = str(float(leftPart.right.value) * float(expression.right.value))
                                else:
                                    newValue = str(float(leftPart.right.value) / float(expression.right.value))
                                rightPart = Literals.Double(leftPart.right.lineNr,leftPart.right.positionNr,newValue)
                                return Expression.BinOp(expression.lineNr,expression.positionNr,expression.operator,leftPart.left,rightPart)
                            else:
                                expression.left = leftPart
                                return expression
                        else:
                            if (expression.operator.value == "+"):
                                newValue = str(float(leftPart.value) + float(expression.right.value))
                            elif (expression.operator.value == "-"):
                                newValue = str(float(leftPart.value) - float(expression.right.value))
                            elif (expression.operator.value == "*"):
                                newValue = str(float(leftPart.value) * float(expression.right.value))
                            else:
                                newValue = str(float(leftPart.value) / float(expression.right.value))
                            return Literals.Double(expression.lineNr, expression.positionNr,newValue)
                    elif(isinstance(expression.right,Expression.BinOp)):
                        rightPart=self.constantFolding(basicType,expression.right)
                        if(isinstance(rightPart,Literals.Double)):
                            if (isinstance(leftPart, Expression.BinOp)):
                                if (isinstance(leftPart.right, Literals.Double)):
                                    if (expression.operator.value == "+"):
                                        newValue = str(float(leftPart.right.value) + float(rightPart.value))
                                    elif (expression.operator.value == "-"):
                                        newValue = str(float(leftPart.right.value) - float(rightPart.value))
                                    elif (expression.operator.value == "*"):
                                        newValue = str(float(leftPart.right.value) * float(rightPart.value))
                                    else:
                                        newValue = str(float(leftPart.right.value) / float(rightPart.value))
                                    rightPart = Literals.Double(leftPart.right.lineNr, leftPart.right.positionNr, newValue)
                                    return Expression.BinOp(expression.lineNr, expression.positionNr, expression.operator,leftPart.left, rightPart)
                                else:
                                    expression.left = leftPart
                                    expression.right = rightPart
                                    return expression
                            else:
                                if (expression.operator.value == "+"):
                                    newValue = str(float(leftPart.value) + float(rightPart.value))
                                elif (expression.operator.value == "-"):
                                    newValue = str(float(leftPart.value) - float(rightPart.value))
                                elif (expression.operator.value == "*"):
                                    newValue = str(float(leftPart.value) * float(rightPart.value))
                                else:
                                    newValue = str(float(leftPart.value) / float(rightPart.value))
                                return Literals.Double(expression.lineNr, expression.positionNr, newValue)
                        else:
                            expression.left=leftPart
                            expression.right=rightPart
                            return expression
                    else:
                        expression.left=leftPart
                        return expression
                else:
                    if(isinstance(expression.left, Literals.Double)):
                        if(isinstance(expression.right, Literals.Double)):
                            if(expression.operator.value=="+"):
                                newValue = str(float(expression.left.value) + float(expression.right.value))
                            elif(expression.operator.value=="-"):
                                newValue = str(float(expression.left.value) - float(expression.right.value))
                            elif(expression.operator.value=="*"):
                                newValue = str(float(expression.left.value) * float(expression.right.value))
                            else:
                                newValue = str(float(expression.left.value) / float(expression.right.value))
                            return Literals.Double(expression.lineNr,expression.positionNr,newValue)
                        elif(isinstance(expression.right,Expression.BinOp)):
                            rightPart=self.constantFolding(basicType,expression.right)
                            if(isinstance(rightPart,Literals.Double)):
                                if (expression.operator.value == "+"):
                                    newValue = str(float(expression.left.value) + float(rightPart.value))
                                elif (expression.operator.value == "-"):
                                    newValue = str(float(expression.left.value) - float(rightPart.value))
                                elif (expression.operator.value == "*"):
                                    newValue = str(float(expression.left.value) * float(rightPart.value))
                                else:
                                    newValue = str(float(expression.left.value) / float(rightPart.value))
                                return Literals.Double(expression.lineNr, expression.positionNr, newValue)
                            else:
                                expression.right=rightPart
                                return expression
                        else:
                            return expression
                    else:
                        if(isinstance(expression.right,Expression.BinOp)):
                            expression.right = self.constantFolding(basicType,expression.right)
                        return expression
        else:
            return expression

    def eraseNullSequences(self,expression):
        if(isinstance(expression,Expression.BinOp)):
            if(isinstance(expression.left,Literals.Int) or isinstance(expression.left,Literals.Double)):
                if (((expression.operator.value == "+" or expression.operator.value == "-") and (expression.left.value == "0" or expression.left.value == "0.0")) or (expression.operator.value == "*" and (expression.left.value == "1" or expression.left.value == "1.0"))):
                    return self.eraseNullSequences(expression.right)
                else:
                    expression.right= self.eraseNullSequences(expression.right)
                    return expression
            elif(isinstance(expression.left,Expression.BinOp)):
                leftPart = self.eraseNullSequences(expression.left)
                if(isinstance(leftPart,Literals.Int) or isinstance(leftPart,Literals.Double)):
                    if (((expression.operator.value == "+" or expression.operator.value == "-") and (leftPart.value == "0" or leftPart.value == "0.0")) or (expression.operator.value == "*" and (leftPart.value == "1" or leftPart.value == "1.0"))):
                        return self.eraseNullSequences(expression.right)
                    else:
                        expression.right = self.eraseNullSequences(expression.right)
                        return expression
                else:
                    if (isinstance(expression.right, Literals.Int) or isinstance(expression.right,Literals.Double)):
                        if (((expression.operator.value == "+" or expression.operator.value == "-") and (expression.right.value == "0" or expression.right.value == "0.0")) or (expression.operator.value == "*" and (expression.right.value == "1" or expression.left.right == "1.0")) or (expression.operator.value == "/" and (expression.right.value == "1" or expression.right.value == "1.0"))):
                            return leftPart
                        else:
                            expression.left=leftPart
                            return expression
                    elif (isinstance(expression.right, Expression.BinOp)):
                        expression.left =leftPart
                        expression.right = self.eraseNullSequences(expression.right)
                        return expression
                    else:
                        expression.left=leftPart
                        return expression
            else:
                if(isinstance(expression.right,Literals.Int) or isinstance(expression.right,Literals.Double)):
                    if (((expression.operator.value == "+" or expression.operator.value == "-") and (expression.right.value == "0" or expression.right.value == "0.0")) or (expression.operator.value == "*" and (expression.right.value == "1" or expression.right.value == "1.0")) or(expression.operator.value=="/" and (expression.right.value=="1"or expression.right.value == "1.0"))):
                        return expression.left
                    else:
                        return expression
                elif(isinstance(expression.right,Expression.BinOp)):
                    expression.right=self.eraseNullSequences(expression.right)
                    return expression
                else:
                    return expression
        else:
            return expression