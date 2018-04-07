
import sys
from antlr4 import *
from CLexer import CLexer
from CParser import CParser
from ParseTreeVisitor import ParseTreeVisitor


def main(argv):
    inputFile = FileStream(argv[1])
    
    lexer = CLexer(inputFile)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.prog()

    # Build AST with the generated parse tree
    parseTreeVisitor = ParseTreeVisitor()
    parseTreeVisitor.generateDOT(parser, tree)


if __name__ == '__main__':
    main(sys.argv)