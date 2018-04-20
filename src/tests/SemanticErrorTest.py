import sys
import os
sys.path.append("..")

import unittest
from antlr4 import *
from CLexer import CLexer
from CParser import CParser
from ASTBuilder import ASTBuilder
from SemanticValidator import SemanticValidator


class SyntaxErrorTestCase(unittest.TestCase):

    def semanticAnalyse(self, file):
        lexer = CLexer(FileStream(os.path.dirname(os.path.abspath(__file__)) + "/" + file))
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        tree = parser.prog()

        astBuilder = ASTBuilder()
        AST = astBuilder.visit(tree)

        semanticValidator = SemanticValidator()
        AST.accept(semanticValidator)

        return semanticValidator.errors

    def test_undefinedRefToVar(self):
        errors = self.semanticAnalyse("data/SemanticErrors/UndefinedRefToVar.c")
        self.assertEqual(errors[0], "Line 6 at 5: Undefined reference to 'a'")

    def test_undefinedRefToFunc(self):
        errors = self.semanticAnalyse("data/SemanticErrors/UndefinedRefToFunc.c")
        self.assertEqual(errors[0], "Line 6 at 5: Undefined reference to 'f'")

    def test_redefinitionVar(self):
        errors = self.semanticAnalyse("data/SemanticErrors/RedefinitionVar.c")
        self.assertEqual(errors[0], "Line 7 at 9: Redefinition of 'a'")

    def test_redefinitionFunc(self):
        errors = self.semanticAnalyse("data/SemanticErrors/RedefinitionFunc.c")
        self.assertEqual(errors[0], "Line 6 at 1: Redefinition of 'f'")

    def test_nestedScope(self):
        errors = self.semanticAnalyse("data/SemanticErrors/NestedScope.c")
        self.assertEqual(errors[0], "Line 9 at 5: Undefined reference to 'b'")

    def test_subscriptNotArray(self):
        errors = self.semanticAnalyse("data/SemanticErrors/SubscriptNotArray.c")
        self.assertEqual(errors[0], "Line 7 at 5: Subscripted value 'a' is not an array")




if __name__ == '__main__':
    unittest.main()
