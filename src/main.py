
import sys
from antlr4 import *
from CLexer import CLexer
from CParser import CParser
from DotGenerators.ParseTreeDotGenerator import ParseTreeDotGenerator
from ASTBuilder import ASTBuilder
from DotGenerators.DotGraphBuilder import DotGraphBuilder
from SemanticValidator import SemanticValidator
from Optimiser import Optimiser

def main(argv):
    inputFile = FileStream(argv[1])
    lexer = CLexer(inputFile)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.prog()

    if parser.getNumberOfSyntaxErrors():
        return

    # Visualise parse tree
    parseTreeDotGen = ParseTreeDotGenerator()
    parseTreeDotGen.generateDOT(parser, tree, "output/parse_tree.gv", render=False)

    # Build AST
    astBuilder = ASTBuilder()
    AST = astBuilder.visit(tree)

    # Semantic Validition
    semanticValidator = SemanticValidator()
    AST.accept(semanticValidator)

    # Print errors, if any
    if semanticValidator.errors:
        for error in semanticValidator.errors:
            print("ERROR: " + error)
        return

    # Code optimiser
    optimiser = Optimiser()
    AST.accept(optimiser)

    # Visualise AST
    dotGraph = AST.visit(DotGraphBuilder)
    dotGraph.render("output/ast.gv", view=True)


if __name__ == '__main__':
    main(sys.argv)
