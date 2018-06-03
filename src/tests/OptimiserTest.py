import sys
import os
sys.path.append("..")

import unittest
from antlr4 import *
from CLexer import CLexer
from CParser import CParser
from ASTBuilder import ASTBuilder
from SemanticValidator import SemanticValidator
from Optimiser import Optimiser
from AST import Expression, Function, Literals, Program, Statement, Variable
from copy import deepcopy


class OptimiserTestCase(unittest.TestCase):

    def semanticAnalyse(self, file):
        lexer = CLexer(FileStream(os.path.dirname(os.path.abspath(__file__)) + "/" + file))
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        tree = parser.prog()

        astBuilder = ASTBuilder()
        AST = astBuilder.visit(tree)
        oldAST = deepcopy(AST)

        semanticValidator = SemanticValidator()
        AST.accept(semanticValidator)

        optimiser = Optimiser(semanticValidator.symbolTable)
        AST.accept(optimiser)

        return optimiser.warnings, oldAST, AST

    def test_unusedVar(self):
        warnings, oldAST, AST = self.semanticAnalyse("data/Optimiser/UnusedVar.c")
        self.assertEqual(warnings[0], "Line 6 at 5: Unused variable 'a'")

        hasVar = False
        for decl in oldAST.declarationList.declarations[0].body.localDecls:     # Search in main function
            if type(decl) is Variable.VariableDecl:
                hasVar = True
        self.assertTrue(hasVar)

        hasVar = False
        for decl in AST.declarationList.declarations[0].body.localDecls:     # Search in main function
            if type(decl) is Variable.VariableDecl:
                hasVar = True
        self.assertFalse(hasVar)

    def test_unusedFunction(self):
        warnings, oldAST, AST = self.semanticAnalyse("data/Optimiser/UnusedFunction.c")
        self.assertEqual(warnings[0], "Line 2 at 1: Unused function 'f'")

        # Two function decls: main() and f()
        self.assertEqual(len(oldAST.declarationList.declarations), 2)

        # Only one function decl: main()
        self.assertEqual(len(AST.declarationList.declarations), 1)

    def test_unreachableReturn(self):
        warnings, oldAST, AST = self.semanticAnalyse("data/Optimiser/UnreachableReturn.c")
        self.assertEqual(warnings[0], "Line 5 at 1: Unreachable code after return")

        # Check the nr of statements in the main function before and after
        self.assertEqual(len(oldAST.declarationList.declarations[0].body.statements), 2)
        self.assertEqual(len(AST.declarationList.declarations[0].body.statements), 1)

    def test_unreachableBreak(self):
        warnings, oldAST, AST = self.semanticAnalyse("data/Optimiser/UnreachableBreak.c")
        self.assertEqual(warnings[0], "Line 7 at 5: Unreachable code after break")

        # Check the nr of statements in the while loop before and after
        self.assertEqual(len(oldAST.declarationList.declarations[0].body.statements[0].body.statements), 2)
        self.assertEqual(len(AST.declarationList.declarations[0].body.statements[0].body.statements), 1)

    def test_nullSequence(self):
        warnings, oldAST, AST = self.semanticAnalyse("data/Optimiser/NullSequence.c")

        self.assertIs(type(oldAST.declarationList.declarations[0].body.statements[0].expression.right), Expression.BinOp)
        self.assertIs(type(AST.declarationList.declarations[0].body.statements[0].expression.right), Expression.Mutable)

        self.assertIs(type(oldAST.declarationList.declarations[0].body.statements[1].expression.right), Expression.BinOp)
        self.assertIs(type(AST.declarationList.declarations[0].body.statements[1].expression.right), Expression.Mutable)

    def test_constantFolding(self):
        warnings, oldAST, AST = self.semanticAnalyse("data/Optimiser/ConstantFolding.c")

        self.assertIs(type(oldAST.declarationList.declarations[0].body.statements[0].expression.right), Expression.BinOp)
        self.assertIs(type(AST.declarationList.declarations[0].body.statements[0].expression.right), Literals.Int)

        self.assertIs(type(oldAST.declarationList.declarations[0].body.statements[1].expression.right), Expression.BinOp)
        self.assertIs(type(AST.declarationList.declarations[0].body.statements[1].expression.right), Literals.Int)

        self.assertIs(type(oldAST.declarationList.declarations[0].body.statements[2].expression.right), Expression.BinOp)
        self.assertIs(type(AST.declarationList.declarations[0].body.statements[2].expression.right), Literals.Int)


if __name__ == '__main__':
    unittest.main()
