
from ASTListener import ASTListener
from SymbolTable.SymbolTable import *
from AST import Expression, Function, Literals, Program, Statement, Variable


class Optimiser(ASTListener):

    def enterCompound(self, node):

        # Check for unreachable code
        for i in range(len(node.statements)):
            if type(node.statements[i]) is Statement.Return:
                del node.statements[i + 1:]
                return True

            # Check if there's a return in the compound state
            elif type(node.statements[i]) is Statement.Compound:
                if self.enterCompound(node.statements[i]):
                    del node.statements[i + 1:]
                    return True

            # Check if there's a return in both the if and else branch
            elif type(node.statements[i]) is Statement.If:
                if node.statements[i].elseBody is not None:
                    returns = 0
                    if type(node.statements[i].body) is Statement.Return:
                        returns += 1
                    elif self.enterCompound(node.statements[i].body):
                        returns += 1
                    if type(node.statements[i].elseBody) is Statement.Return:
                        returns += 1
                    elif self.enterCompound(node.statements[i].elseBody):
                        returns += 1

                    if returns == 2:
                        del node.statements[i + 1:]
                        return True

        return False

    def enterWhile(self, node):

        # Check for unreachable code
        if type(node.body) is Statement.Compound:
            for i in range(len(node.body.statements)):
                if type(node.body.statements[i]) is Statement.Break:
                    del node.body.statements[i + 1:]
                    break
        # Still need to check for break's inside other statements..., no easy way to do it...
