

import unittest
from antlr4 import *
from src.CLexer import CLexer
from src.CParser import CParser


class SyntaxErrorTestCase(unittest.TestCase):

    def test_missingSemiColon(self):
        lexer = CLexer(FileStream("data/MissingSemiColon.c"))
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        parser.prog()

        self.assertEqual(parser.getNumberOfSyntaxErrors(), 1)

    def test_missingBracket(self):
        lexer = CLexer(FileStream("data/MissingBracket.c"))
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        parser.prog()

        self.assertEqual(parser.getNumberOfSyntaxErrors(), 1)

    def test_wrongKeyword(self):
        lexer = CLexer(FileStream("data/WrongKeyword.c"))
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        parser.prog()

        self.assertEqual(parser.getNumberOfSyntaxErrors(), 1)


if __name__ == '__main__':
    unittest.main()
