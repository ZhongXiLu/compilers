import sys
sys.path.append("..")

import unittest
from antlr4 import *
from CLexer import CLexer
from CParser import CParser


class SyntaxErrorTestCase(unittest.TestCase):

    def parse(self, file):
        lexer = CLexer(FileStream(file))
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        parser.prog()

        return parser.getNumberOfSyntaxErrors()

    def test_missingSemiColon(self):
        self.assertEqual(self.parse("data/SyntaxErrors/MissingSemiColon.c"), 1)

    def test_missingBracket(self):
        self.assertEqual(self.parse("data/SyntaxErrors/MissingBracket.c"), 1)

    def test_wrongKeyword(self):
        self.assertEqual(self.parse("data/SyntaxErrors/WrongKeyword.c"), 1)

    def test_wrongIfConstruction(self):
        self.assertEqual(self.parse("data/SyntaxErrors/WrongIfConstruction.c"), 1)


if __name__ == '__main__':
    unittest.main()
