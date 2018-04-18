
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

from CVisitor import CVisitor
from AST import Expression, Function, Literals, Program, Statement, Variable


class ASTBuilder(CVisitor):

    # Visit a parse tree produced by CParser#prog.
    def visitProg(self, ctx: CParser.ProgContext):
        includes = Program.Includes(ctx.start.line, ctx.start.column, self.visitIncludes(ctx.includes()))
        declarationList = Program.DeclarationList(ctx.start.line, ctx.start.column, self.visitDeclarationList(ctx.declarationList()))
        return Program.Program(ctx.start.line, ctx.start.column, includes, declarationList)

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
        return Program.Include(ctx.start.line, ctx.start.column, ctx.Library().getText())

    # Visit a parse tree produced by CParser#varDeclaration.
    def visitVarDeclaration(self, ctx:CParser.VarDeclarationContext):
        type = self.visitTypeSpecifier(ctx.typeSpecifier())
        varDeclList = Variable.VarDeclList(ctx.start.line, ctx.start.column, self.visitVarDeclList(ctx.varDeclList()))
        return Variable.VariableDecl(ctx.start.line, ctx.start.column, type, varDeclList)

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
        # Check if it's an array initialization
        try:
            size = ctx.IntConst().getText()
            initializeList = None
            try:
                initializeList = Variable.ArrayInitialize(ctx.start.line, ctx.start.column, self.visitArrayInitialize(ctx.arrayInitialize()))
            except:
                pass
            return Variable.Array(ctx.start.line, ctx.start.column, name, size, initializeList)

        except:
            expression = None
            try:
                expression = self.visitSimpleExpression(ctx.simpleExpression())
            except:
                pass
            return Variable.VarDeclInitialize(ctx.start.line, ctx.start.column, name, expression)

    # Visit a parse tree produced by CParser#arrayInitialize.
    def visitArrayInitialize(self, ctx:CParser.ArrayInitializeContext):
        initializeList = []
        try:
            initializeList += self.visitArrayInitialize(ctx.arrayInitialize())
            initializeList.append(self.visitSimpleExpression(ctx.simpleExpression()))
        except:
            pass
        return initializeList

    # Visit a parse tree produced by CParser#typeSpecifier.
    def visitTypeSpecifier(self, ctx:CParser.TypeSpecifierContext):
        return ctx.getText()

    # Visit a parse tree produced by CParser#funcDeclaration.
    def visitFuncDeclaration(self, ctx:CParser.FuncDeclarationContext):
        name = ctx.Id().getText()
        typeSpecifier =  self.visitFunctionTypeSpecifier(ctx.functionTypeSpecifier())
        params = self.visitParams(ctx.params())
        body = self.visitCompoundStmt(ctx.compoundStmt())
        return Function.FunctionDecl(ctx.start.line, ctx.start.column, name, params, body, typeSpecifier)

    # Visit a parse tree produced by CParser#functionTypeSpecifier.
    def visitFunctionTypeSpecifier(self, ctx:CParser.FunctionTypeSpecifierContext):
        try:
            return self.visitTypeSpecifier(ctx.typeSpecifier())
        except:
            pass
        return ctx.getText()

    # Visit a parse tree produced by CParser#params.
    def visitParams(self, ctx:CParser.ParamsContext):
        return Function.Parameters(ctx.start.line, ctx.start.column, self.visitParamList(ctx.paramList()))

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
        return Function.Parameter(ctx.start.line, ctx.start.column, typeSpecifier, name)

    # Visit a parse tree produced by CParser#expression.
    def visitExpression(self, ctx:CParser.ExpressionContext):
        try:
            left = self.visitMutable(ctx.mutable())
            right = self.visitExpression(ctx.expression())
            return Expression.Assign(ctx.start.line, ctx.start.column, left, right)
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
            return Expression.BinOp(ctx.start.line, ctx.start.column, operator, left, right)
        except:
            return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#andExpression.
    def visitAndExpression(self, ctx:CParser.AndExpressionContext):
        try:
            operator = Expression.BinOpTokens.AND
            left = self.visitAndExpression(ctx.andExpression())
            right = self.visitUnaryRelExpression(ctx.unaryRelExpression())
            return Expression.BinOp(ctx.start.line, ctx.start.column, operator, left, right)
        except:
            return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#unaryRelExpression.
    def visitUnaryRelExpression(self, ctx: CParser.UnaryRelExpressionContext):
        try:
            operator = Expression.UnaryOpTokens.NEG
            operand = self.visitUnaryRelExpression(ctx.unaryRelExpression())
            return Expression.UnaryOp(ctx.start.line, ctx.start.column, operator, operand)
        except:
            return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#relExpression.
    def visitRelExpression(self, ctx:CParser.RelExpressionContext):
        try:
            operator = Expression.BinOpTokens(self.visitRelOp(ctx.relOp()))
            left = self.visitSumExpression(ctx.sumExpression(0))
            right = self.visitSumExpression(ctx.sumExpression(1))
            return Expression.BinOp(ctx.start.line, ctx.start.column, operator, left, right)
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
            return Expression.BinOp(ctx.start.line, ctx.start.column, operator, left, right)
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
            return Expression.BinOp(ctx.start.line, ctx.start.column, operator, left, right)
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
            return Expression.UnaryOp(ctx.start.line, ctx.start.column, operator, operand)
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
        return Statement.Compound(ctx.start.line, ctx.start.column, localDecls, statements)

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
        return Statement.ExpressionStmt(ctx.start.line, ctx.start.column, expression)

    # Visit a parse tree produced by CParser#selectionStmt.
    def visitSelectionStmt(self, ctx:CParser.SelectionStmtContext):
        expression = self.visitSimpleExpression(ctx.simpleExpression())
        body = self.visitStatement(ctx.statement(0))
        elseBody = None
        try:
            elseBody = self.visitStatement(ctx.statement(1))
        except:
            pass
        return Statement.If(ctx.start.line, ctx.start.column, expression, body, elseBody)

    # Visit a parse tree produced by CParser#iterationStmt.
    def visitIterationStmt(self, ctx:CParser.IterationStmtContext):
        expression = self.visitSimpleExpression(ctx.simpleExpression())
        body = self.visitStatement(ctx.statement())
        return Statement.While(ctx.start.line, ctx.start.column, expression, body)

    # Visit a parse tree produced by CParser#returnStmt.
    def visitReturnStmt(self, ctx:CParser.ReturnStmtContext):
        expression = None
        try:
            expression = self.visitExpression(ctx.expression())
        except:
            pass
        return Statement.Return(ctx.start.line, ctx.start.column, expression)

    # Visit a parse tree produced by CParser#breakStmt.
    def visitBreakStmt(self, ctx:CParser.BreakStmtContext):
        return Statement.Break(ctx.start.line, ctx.start.column)

    # Visit a parse tree produced by CParser#mutable.
    def visitMutable(self, ctx:CParser.MutableContext):
        try:
            return Expression.Mutable(ctx.start.line, ctx.start.column, ctx.Id().getText())
        except:
            pass
        mutable = self.visitMutable(ctx.mutable())
        expression = self.visitExpression(ctx.expression())
        return Expression.SubScript(ctx.start.line, ctx.start.column, mutable, expression)

    # Visit a parse tree produced by CParser#call.
    def visitCall(self, ctx:CParser.CallContext):
        funcName = ctx.Id().getText()
        args = self.visitArgs(ctx.args())
        return Expression.Call(ctx.start.line, ctx.start.column, funcName, args)

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
            return Literals.Int(ctx.start.line, ctx.start.column, ctx.IntConst().getText())
        except:
            pass
        try:
            return Literals.Double(ctx.start.line, ctx.start.column, ctx.DoubleConst().getText())
        except:
            pass
        return Literals.String(ctx.start.line, ctx.start.column, ctx.CharConst().getText())
