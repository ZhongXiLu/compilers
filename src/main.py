
import sys
from antlr4 import *
from CLexer import CLexer
from CParser import CParser
from DotGenerators.ParseTreeDotGenerator import ParseTreeDotGenerator
from ASTBuilder import ASTBuilder
from DotGenerators.DotGraphBuilder import DotGraphBuilder
from SemanticValidator import SemanticValidator

def main(argv):
    #inputFile = FileStream(argv[1])
    inputFile = FileStream("examples/example3.c")
    lexer = CLexer(inputFile)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.prog()

    # Visualise parse tree
    parseTreeDotGen = ParseTreeDotGenerator()
    parseTreeDotGen.generateDOT(parser, tree, "output/parse_tree.gv", render=True)

    # Build AST
    astBuilder = ASTBuilder()
    AST = astBuilder.visit(tree)

    # Visualise AST
    dotGraph = AST.visit(DotGraphBuilder)
    dotGraph.render("output/ast.gv", view=True)

    # Semantic Validition
    semanticValidator = SemanticValidator()
    AST.accept(semanticValidator)

    # Print errors, if any
    for error in semanticValidator.errors:
        print("ERROR: " + error)

if __name__ == '__main__':
    main(sys.argv)
