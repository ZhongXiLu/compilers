
from ASTListener import ASTListener
from SymbolTable.SymbolTable import *
from AST import Expression, Function, Literals, Program, Statement, Variable


class Optimiser(ASTListener):

    def __init__(self, symbolTable):
        self.symbolTable = symbolTable

    def enterProgram(self, node):
        self.symbolTable.currentScope.currentChild += 1
        self.symbolTable.currentScope = self.symbolTable.currentScope.children[self.symbolTable.currentScope.currentChild-1]

        # Check for unused functions
        i = 0
        while i < len(node.declarationList.declarations):
            if type(node.declarationList.declarations[i]) is Function.FunctionDef or \
                    type(node.declarationList.declarations[i]) is Function.FunctionDecl:
                # Note: main function is exception
                if node.declarationList.declarations[i].name != "main" and \
                        not self.symbolTable.getSymbol(node.declarationList.declarations[i].name).used:
                    del node.declarationList.declarations[i]
                    i -= 1
            i += 1

    def exitProgram(self, node):
        self.symbolTable.currentScope = self.symbolTable.currentScope.parent

    def returnInCompund(self, node):
        # Check for unreachable code
        for i in range(len(node.statements)):
            if type(node.statements[i]) is Statement.Return:
                del node.statements[i + 1:]
                return True

            # Check if there's a return in the compound state
            elif type(node.statements[i]) is Statement.Compound:
                if self.returnInCompund(node.statements[i]):
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
                        del node.statements[i + 1:]
                        return True

        return False

    def enterCompound(self, node):
        self.symbolTable.currentScope.currentChild += 1
        self.symbolTable.currentScope = self.symbolTable.currentScope.children[self.symbolTable.currentScope.currentChild-1]

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
                    del node.body.statements[i + 1:]
                    break
        # Still need to check for break's inside other statements..., no easy way to do it...

    def enterFunctionDef(self, node):
        self.symbolTable.currentScope.currentChild += 1
        self.symbolTable.currentScope = self.symbolTable.currentScope.children[self.symbolTable.currentScope.currentChild-1]

    def exitFunctionDef(self, node):
        self.symbolTable.currentScope = self.symbolTable.currentScope.parent

    def enterVarDeclList(self, node):

        # Check for unused variables
        i = 0
        while i < len(node.declInitializeList):
            if type(node.declInitializeList[i]) is Variable.VarDeclInitialize or \
                    type(node.declInitializeList[i]) is Function.ArrayInitialize:
                if not self.symbolTable.getSymbol(node.declInitializeList[i].name).used:
                    del node.declInitializeList[i]
                    i -= 1
            i += 1
