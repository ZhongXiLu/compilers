import sys
import os
sys.path.append("..")

import unittest
from antlr4 import *
from CLexer import CLexer
from CParser import CParser
from ASTBuilder import ASTBuilder
from SemanticValidator import SemanticValidator


class TypeErrorTestCase(unittest.TestCase):

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

    def test_assingIntToChar(self):
        errors = self.semanticAnalyse("data/TypeErrors/AssignIntToChar.c")
        self.assertEqual(errors[0], "Line 6 at 11: Type mismatch: expected 'char' but found 'int'")

    def test_assignIntToString(self):
        errors = self.semanticAnalyse("data/TypeErrors/AssignIntToString.c")
        self.assertEqual(errors[0], "Line 6 at 12: Type mismatch: expected 'char*' but found 'int'")

    def test_assignStringToInt(self):
        errors = self.semanticAnalyse("data/TypeErrors/AssignStringToInt.c")
        self.assertEqual(errors[0], "Line 6 at 10: Type mismatch: expected 'int' but found 'string'")

    def test_IntPlusString(self):
        errors = self.semanticAnalyse("data/TypeErrors/IntPlusString.c")
        self.assertEqual(errors[0], "Line 6 at 14: Type mismatch: expected 'int' but found 'string'")


if __name__ == '__main__':
    unittest.main()
