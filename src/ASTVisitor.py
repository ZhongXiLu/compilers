
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

from CVisitor import CVisitor
from AST import Function, Program


class ASTVisitor(CVisitor):

    # Visit a parse tree produced by CParser#prog.
    def visitProg(self, ctx: CParser.ProgContext):
        includes = Program.Includes(self.visitIncludes(ctx.includes()))
        declarationList = Program.DeclarationList(self.visitDeclarationList(ctx.declarationList()))
        return Program.Program(includes, declarationList)

    # Visit a parse tree produced by CParser#declarationList.
    def visitDeclarationList(self, ctx:CParser.DeclarationListContext):
        declarations = []
        try:
            declarations += self.visitDeclarationList(ctx.declarationList())
            declarations.append(self.visit(ctx.declaration()))
        except:
            pass
        return declarations

    # Visit a parse tree produced by CParser#declaration.
    def visitDeclaration(self, ctx:CParser.DeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#includes.
    def visitIncludes(self, ctx: CParser.IncludesContext):
        includes = []
        try:
            includes += self.visitIncludes(ctx.includes())
            includes.append(self.visitInclude(ctx.include()))
        except:
            pass
        return includes

    # Visit a parse tree produced by CParser#include.
    def visitInclude(self, ctx: CParser.IncludeContext):
        return Program.Include(ctx.Library().getText())

    # Visit a parse tree produced by CParser#typeSpecifier.
    def visitTypeSpecifier(self, ctx:CParser.TypeSpecifierContext):
        return ctx.getText()

    # Visit a parse tree produced by CParser#funcDeclaration.
    def visitFuncDeclaration(self, ctx:CParser.FuncDeclarationContext):
        name = ctx.Id().getText()
        typeSpecifier =  self.visitTypeSpecifier(ctx.typeSpecifier())
        args = self.visitParams(ctx.params())
        body = self.visitCompoundStmt(ctx.compoundStmt())
        return Function.Function(name, args, body, typeSpecifier)

    # Visit a parse tree produced by CParser#params.
    def visitParams(self, ctx:CParser.ParamsContext):
        return Function.Arguments(self.visitParamList(ctx.paramList()))

    # Visit a parse tree produced by CParser#paramList.
    def visitParamList(self, ctx:CParser.ParamListContext):
        params = []
        try:
            params += self.visitParamList(ctx.paramList())
            params.append(self.visitParamTypeList(ctx.paramTypeList()))
        except:
            pass
        return params

    # Visit a parse tree produced by CParser#paramTypeList.
    def visitParamTypeList(self, ctx:CParser.ParamTypeListContext):
        typeSpecifier = self.visitTypeSpecifier(ctx.getChild(0))
        name = ctx.Id().getText()
        return Function.Argument(typeSpecifier, name)
