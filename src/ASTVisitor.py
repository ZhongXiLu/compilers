
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

from CVisitor import CVisitor
from AST import Expression, Function, Literals, Program, Statement, Variable


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
            declarations.append(self.visitDeclaration(ctx.declaration()))
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

    # Visit a parse tree produced by CParser#varDeclaration.
    def visitVarDeclaration(self, ctx:CParser.VarDeclarationContext):
        type = self.visitTypeSpecifier(ctx.typeSpecifier())
        varDeclList = Variable.VarDeclList(self.visitVarDeclList(ctx.varDeclList()))
        return Variable.VariableDecl(type, varDeclList)

    # Visit a parse tree produced by CParser#varDeclList.
    def visitVarDeclList(self, ctx:CParser.VarDeclListContext):
        decls = []
        try:
            decls += self.visitVarDeclList(ctx.varDeclList())
            decls.append(self.visitVarDeclInitialize(ctx.varDeclInitialize()))
        except:
            pass
        return decls

    # Visit a parse tree produced by CParser#varDeclInitialize.
    def visitVarDeclInitialize(self, ctx:CParser.VarDeclInitializeContext):
        name = ctx.Id().getText()
        expression = None
        try:
            expression = self.visitSimpleExpression(ctx.simpleExpression())
        except:
            pass
        return Variable.VarDeclInitialize(name, expression)

    # Visit a parse tree produced by CParser#typeSpecifier.
    def visitTypeSpecifier(self, ctx:CParser.TypeSpecifierContext):
        return ctx.getText()

    # Visit a parse tree produced by CParser#funcDeclaration.
    def visitFuncDeclaration(self, ctx:CParser.FuncDeclarationContext):
        name = ctx.Id().getText()
        typeSpecifier =  self.visitTypeSpecifier(ctx.typeSpecifier())
        params = self.visitParams(ctx.params())
        body = self.visitCompoundStmt(ctx.compoundStmt())
        return Function.FunctionDecl(name, params, body, typeSpecifier)

    # Visit a parse tree produced by CParser#params.
    def visitParams(self, ctx:CParser.ParamsContext):
        return Function.Parameters(self.visitParamList(ctx.paramList()))

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
        return Function.Parameter(typeSpecifier, name)

    # Visit a parse tree produced by CParser#expression.
    def visitExpression(self, ctx:CParser.ExpressionContext):
        try:
            operator = Expression.BinOpTokens.ASSIGN
            left = self.visitMutable(ctx.mutable())
            right = self.visitExpression(ctx.expression())
            return Expression.BinOp(operator, left, right)
        except:
            pass
        try:
            return self.visitExpression(ctx.expression())
        except:
            pass
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#simpleExpression.
    def visitSimpleExpression(self, ctx:CParser.SimpleExpressionContext):
        try:
            operator = Expression.BinOpTokens.OR
            left = self.visitSimpleExpression(ctx.simpleExpression())
            right = self.visitAndExpression(ctx.andExpression())
            return Expression.BinOp(operator, left, right)
        except:
            return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#andExpression.
    def visitAndExpression(self, ctx:CParser.AndExpressionContext):
        try:
            operator = Expression.BinOpTokens.AND
            left = self.visitAndExpression(ctx.andExpression())
            right = self.visitUnaryRelExpression(ctx.unaryRelExpression())
            return Expression.BinOp(operator, left, right)
        except:
            return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#unaryRelExpression.
    def visitUnaryRelExpression(self, ctx: CParser.UnaryRelExpressionContext):
        try:
            operator = Expression.UnaryOpTokens.NEG
            operand = self.visitUnaryRelExpression(ctx.unaryRelExpression())
            return Expression.UnaryOp(operator, operand)
        except:
            return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#relExpression.
    def visitRelExpression(self, ctx:CParser.RelExpressionContext):
        try:
            operator = Expression.BinOpTokens(self.visitRelOp(ctx.relOp()))
            left = self.visitSumExpression(ctx.sumExpression(0))
            right = self.visitSumExpression(ctx.sumExpression(1))
            return Expression.BinOp(operator, left, right)
        except:
            return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#relOp.
    def visitRelOp(self, ctx:CParser.RelOpContext):
        return ctx.getText()

    # Visit a parse tree produced by CParser#sumExpression.
    def visitSumExpression(self, ctx:CParser.SumExpressionContext):
        try:
            operator = Expression.BinOpTokens(self.visitSumOp(ctx.sumOp()))
            left = self.visitSumExpression(ctx.sumExpression())
            right = self.visitTerm(ctx.term())
            return Expression.BinOp(operator, left, right)
        except:
            return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#sumOp.
    def visitSumOp(self, ctx:CParser.SumOpContext):
        return ctx.getText()

    # Visit a parse tree produced by CParser#term.
    def visitTerm(self, ctx:CParser.TermContext):
        try:
            operator = Expression.BinOpTokens(self.visitMulOp(ctx.mulOp()))
            left = self.visitTerm(ctx.term())
            right = self.visitUnaryExpression(ctx.unaryExpression())
            return Expression.BinOp(operator, left, right)
        except:
            return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#mulOp.
    def visitMulOp(self, ctx:CParser.MulOpContext):
        return ctx.getText()

    # Visit a parse tree produced by CParser#unaryExpression.
    def visitUnaryExpression(self, ctx:CParser.UnaryExpressionContext):
        try:
            operator = Expression.UnaryOpTokens(self.visitUnaryOp(ctx.unaryOp()))
            operand = self.visitUnaryExpression(ctx.unaryExpression())
            return Expression.UnaryOp(operator, operand)
        except:
            return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#unaryOp.
    def visitUnaryOp(self, ctx:CParser.UnaryOpContext):
        return ctx.getText()

    # Visit a parse tree produced by CParser#compoundStmt.
    def visitCompoundStmt(self, ctx:CParser.CompoundStmtContext):
        localDecls = []
        statements = []
        try:
            statements += self.visitStatementList(ctx.statementList())
        except:
            pass
        try:
            localDecls += self.visitLocalDeclarations(ctx.localDeclarations())
        except:
            pass
        return Statement.Compound(localDecls, statements)

    # Visit a parse tree produced by CParser#localDeclarations.
    def visitLocalDeclarations(self, ctx:CParser.LocalDeclarationsContext):
        decls = []
        try:
            decls += self.visitLocalDeclarations(ctx.localDeclarations())
            decls.append(self.visitVarDeclaration(ctx.varDeclaration()))
        except:
            pass
        return decls

    # Visit a parse tree produced by CParser#statementList.
    def visitStatementList(self, ctx:CParser.StatementListContext):
        statements = []
        try:
            statements += self.visitStatementList(ctx.statementList())
            statements.append(self.visitStatement(ctx.statement()))
        except:
            pass
        return statements

    # Visit a parse tree produced by CParser#expressionStmt.
    def visitExpressionStmt(self, ctx:CParser.ExpressionStmtContext):
        expression = self.visitExpression(ctx.expression())
        return Statement.ExpressionStmt(expression)

    # Visit a parse tree produced by CParser#selectionStmt.
    def visitSelectionStmt(self, ctx:CParser.SelectionStmtContext):
        expression = self.visitSimpleExpression(ctx.simpleExpression())
        body = self.visitStatement(ctx.statement(0))
        elseBody = None
        try:
            elseBody = self.visitStatement(ctx.statement(1))
        except:
            pass
        return Statement.If(expression, body, elseBody)

    # Visit a parse tree produced by CParser#iterationStmt.
    def visitIterationStmt(self, ctx:CParser.IterationStmtContext):
        expression = self.visitSimpleExpression(ctx.simpleExpression())
        body = self.visitStatement(ctx.statement())
        return Statement.While(expression, body)

    # Visit a parse tree produced by CParser#returnStmt.
    def visitReturnStmt(self, ctx:CParser.ReturnStmtContext):
        expression = None
        try:
            expression = self.visitExpression(ctx.expression())
        except:
            pass
        return Statement.Return(expression)

    # Visit a parse tree produced by CParser#breakStmt.
    def visitBreakStmt(self, ctx:CParser.BreakStmtContext):
        return Statement.Break()

    # Visit a parse tree produced by CParser#mutable.
    def visitMutable(self, ctx:CParser.MutableContext):
        try:
            return Expression.Mutable(ctx.Id().getText())
        except:
            pass
        mutable = self.visitMutable(ctx.mutable())
        expression = self.visitExpression(ctx.expression())
        return Expression.SubScript(mutable, expression)

    # Visit a parse tree produced by CParser#call.
    def visitCall(self, ctx:CParser.CallContext):
        funcName = ctx.Id().getText()
        args = self.visitArgs(ctx.args())
        return Expression.Call(funcName, args)

    # Visit a parse tree produced by CParser#args.
    def visitArgs(self, ctx:CParser.ArgsContext):
        args = []
        try:
            args += self.visitArgs(ctx.args())
            args.append(self.visitExpression(ctx.expression()))
        except:
            pass
        return args

    # Visit a parse tree produced by CParser#constant.
    def visitConstant(self, ctx:CParser.ConstantContext):
        try:
            return Literals.Number(ctx.NumConst().getText())
        except:
            pass
        return Literals.String(ctx.CharConst().getText())
