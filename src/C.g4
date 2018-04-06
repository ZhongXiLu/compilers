
// based on: http://marvin.cs.uidaho.edu/Teaching/CS445/c-Grammar.pdf

grammar C;

// ===============================================
// Main Program Rules
// ===============================================

prog: declarationList+;

declarationList
	: declarationList declaration
	| declaration
	;

declaration
	: varDeclaration
	| funcDeclaration
	;

// ===============================================
// Include Rules
// ===============================================

include
	: '#include' '<' library '>'
	;

library
	: 'stdio.h'
	;

// ===============================================
// Variable Rules
// ===============================================

varDeclaration
	: typeSpecifier varDeclList
	;

varDeclList
	: varDeclList ',' varDeclInitialize
	| varDeclInitialize
	;

varDeclInitialize
	: varDeclId
	| varDeclId ':' simpleExpression
	;

varDeclId: ID;

// ===============================================
// Functions Rules
// ===============================================

funcDeclaration
	: typeSpecifier ID '(' params ')' statement
	| ID '(' params ')' statement
	;

params
	: paramList
	| // empty
	;

paramList
	: paramList ';' paramTypeList
	| paramTypeList
	;

paramTypeList
	: typeSpecifier paramIdList
	;

paramIdList
	: paramIdList ',' paramId
	| paramId
	;

paramId: ID;

// ===============================================
// Statement Rules
// ===============================================

statement
	: expressionStmt
	| compoundStmt
	| selectionStmt
	| iterationStmt
	| returnStmt
	| breakStmt
	;

expressionStmt
	: expression ';'
	| ';'
	;

compoundStmt
	: '{' localDeclarations statementList '}'
	;

localDeclarations
	: localDeclarations varDeclaration
	| // empty
	;

statementList
	: statementList statement
	| // empty
	;

selectionStmt
	: 'if' '(' simpleExpression ')' statement
	| 'if' '(' simpleExpression ')' statement 'else' statement
	;

iterationStmt
	: 'while' '(' simpleExpression ')' statement
	;

returnStmt
	: 'return' ';'
	| 'return' expression ';'
	;

breakStmt
	: 'break' ';'
	;

// ===============================================
// Expression Rules
// ===============================================

expression
	: // TODO
	;

simpleExpression
	: // TODO
	;

// ===============================================
// Tokens
// TODO: replace '...' with tokens (e.g. ';' => 'SEMICOLON: ';';')
// ===============================================

typeSpecifier
	: 'char'
	| 'short'
	| 'int'
	| 'long'
	| 'float'
	| 'double'
	| 'signed'
	| 'unsigned'
	| typeSpecifier pointer
	;

pointer: '*';
ID: ('a'..'z'|'A'..'Z'|'_') ('a'..'z'|'A'..'Z'|'0'..'9')*;

// ===============================================
// Comments & Other
// ===============================================

Whitespace
	: [ \t]+
		-> skip
	;

Newline
	: ('\r' '\n'? | '\n') -> skip
	;

BlockComment
	: '/*' .*? '*/'
		-> skip
	;

LineComment
	: '//' ~[\r\n]*
		-> skip
	;