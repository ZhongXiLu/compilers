import sys
import os
sys.path.append("..")

import unittest
from antlr4 import *
from CLexer import CLexer
from CParser import CParser


class CorrectSyntaxTestCase(unittest.TestCase):

    def parse(self, file):
        lexer = CLexer(FileStream(os.path.dirname(os.path.abspath(__file__)) + "/" + file))
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        parser.prog()

        return parser.getNumberOfSyntaxErrors()

    def test_variables(self):
        self.assertEqual(self.parse("data/CorrectSyntax/Variables.c"), 0)

    def test_functions(self):
        self.assertEqual(self.parse("data/CorrectSyntax/Functions.c"), 0)

    def test_statements(self):
        self.assertEqual(self.parse("data/CorrectSyntax/Statements.c"), 0)

    def test_expressions(self):
        self.assertEqual(self.parse("data/CorrectSyntax/Expressions.c"), 0)


if __name__ == '__main__':
    unittest.main()
