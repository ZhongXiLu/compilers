
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

from CVisitor import CVisitor
from AST import Function


class ASTVisitor(CVisitor):


    # Visit a parse tree produced by CParser#typeSpecifier.
    def visitTypeSpecifier(self, ctx:CParser.TypeSpecifierContext):
        return ctx.getText()

    # Visit a parse tree produced by CParser#funcDeclaration.
    def visitFuncDeclaration(self, ctx:CParser.FuncDeclarationContext):
        name = ctx.Id().getText()
        typeSpecifier =  self.visitTypeSpecifier(ctx.getChild(0))
        args = self.visitParams(ctx.getChild(1))
        body = self.visitCompoundStmt(ctx.getChild(2))
        return Function.Function(name, args, body, typeSpecifier)
