
import sys
from antlr4 import *
from CLexer import CLexer
from CParser import CParser
from DotGenerators.ParseTreeDotGenerator import ParseTreeDotGenerator
from ASTVisitor import ASTVisitor
from DotGenerators.DotGraphBuilder import DotGraphBuilder


def main(argv):
    inputFile = FileStream(argv[1])
    
    lexer = CLexer(inputFile)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.prog()

    # Visualise parse tree
    parseTreeDotGen = ParseTreeDotGenerator()
    parseTreeDotGen.generateDOT(parser, tree, "output/parse_tree.gv", render=True)

    # Build AST
    astVisitor = ASTVisitor()
    AST = astVisitor.visit(tree)

    # Visualise AST
    dotGraph = AST.visit(DotGraphBuilder)
    dotGraph.render("output/ast.gv", view=True)


if __name__ == '__main__':
    main(sys.argv)