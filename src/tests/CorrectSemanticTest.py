import sys
import os
sys.path.append("..")

import unittest
from antlr4 import *
from CLexer import CLexer
from CParser import CParser
from ASTBuilder import ASTBuilder
from SemanticValidator import SemanticValidator


class CorrectSemanticTestCase(unittest.TestCase):

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

    def test_correctSemantic1(self):
        errors = self.semanticAnalyse("data/CorrectSemantic/CorrectSemantic1.c")
        self.assertEqual(len(errors), 0)


if __name__ == '__main__':
    unittest.main()
