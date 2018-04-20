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

    def test_assignWrongCallToInt(self):
        errors = self.semanticAnalyse("data/TypeErrors/AssignWrongCallToInt.c")
        self.assertEqual(errors[0], "Line 8 at 10: Type mismatch: expected 'int' but found 'char'")

    def test_assignWrongArrayElementToChar(self):
        errors = self.semanticAnalyse("data/TypeErrors/AssignWrongArrayElementToChar.c")
        self.assertGreater(len(errors), 0)
        # self.assertEqual(errors[0], "Line 8 at 10: Type mismatch: expected 'int' but found 'char'") # TODO

    def test_intPlusString(self):
        errors = self.semanticAnalyse("data/TypeErrors/IntPlusString.c")
        self.assertEqual(errors[0], "Line 6 at 14: Type mismatch: expected 'int' but found 'string'")

    def test_intPlusBool(self):
        errors = self.semanticAnalyse("data/TypeErrors/IntPlusBool.c")
        self.assertGreater(len(errors), 0)
        # self.assertEqual(errors[0], "Line 6 at 17: Type mismatch: expected 'int' but found 'bool'") # TODO

    # TODO: support "double" + "int"?

    def test_negateInt(self):
        errors = self.semanticAnalyse("data/TypeErrors/NegateInt.c")
        self.assertGreater(len(errors), 0)
        # self.assertEqual(errors[0], "Line 6 at 9: Type mismatch: expected 'bool' but found 'int'")  # TODO

    def test_negativeBool(self):
        errors = self.semanticAnalyse("data/TypeErrors/NegativeBool.c")
        self.assertGreater(len(errors), 0)
        # self.assertEqual(errors[0], "Line 6 at 13: Type mismatch: expected 'int' but found 'bool'")  # TODO

    def test_wrongNestedExpressions(self):
        errors = self.semanticAnalyse("data/TypeErrors/WrongNestedExpressions.c")
        self.assertGreater(len(errors), 0)
        # self.assertEqual(errors[0], "Line 6 at 13: Type mismatch: expected 'int' but found 'bool'")  # TODO

    def test_wrongTypeOfParams(self):
        errors = self.semanticAnalyse("data/TypeErrors/WrongTypeOfParams.c")
        self.assertEqual(errors[0], "Line 11 at 5: Wrong parameter type! Expected: 'char' found 'unsigned'")

    def test_wrongTypeOfParams2(self):
        errors = self.semanticAnalyse("data/TypeErrors/WrongTypeOfParams2.c")
        self.assertEqual(errors[0], "Line 8 at 5: Wrong parameter type! Expected: 'char' found 'int'")


if __name__ == '__main__':
    unittest.main()
