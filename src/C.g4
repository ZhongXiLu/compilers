
// based on: http://marvin.cs.uidaho.edu/Teaching/CS445/c-Grammar.pdf

grammar C;

// ===============================================
// Main Program Rules
// ===============================================

prog: includes declarationList;

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

includes
	: includes include
	| include
	| // empty
	;

include
	: '#' 'include' '<' library '>'
	;

library
	: 'stdio.h'
	;

// ===============================================
// Variable Rules
// ===============================================

varDeclaration
	: typeSpecifier varDeclList ';'
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

typeSpecifier
	: 'char'
	| 'short'
	| 'int'
	| 'long'
	| 'float'
	| 'double'
	| 'signed'
	| 'unsigned'
	| typeSpecifier '*'
	;

// ===============================================
// Functions Rules
// ===============================================

funcDeclaration
	: typeSpecifier ID '(' params ')' compoundStmt
	// | ID '(' params ')' compoundStmt 	// TODO: is this correct C ?
	;

params
	: paramList
	| // empty
	;

paramList
	: paramList ',' paramTypeList
	| paramTypeList
	;

paramTypeList
	: typeSpecifier paramIdList
	;

paramIdList: ID;

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
	//| ';'
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
	//| 'return' '0' ';'
	;

breakStmt
	: 'break' ';'
	;

// ===============================================
// Expression Rules
// TODO: make rules shorter?
// ===============================================

// TODO: support '+=', '++', '&&', '%', ...
expression
	: mutable '=' expression
	| simpleExpression
	;

simpleExpression
	: simpleExpression '||' andExpression
	| andExpression
	;

andExpression
	: andExpression '&&' unaryRelExpression
	| unaryRelExpression
	;

unaryRelExpression
	: '!' unaryRelExpression
	| relExpression
	;

relExpression
	: sumExpression relOp sumExpression
	| sumExpression
	;

relOp
	: '<'
	| '>'
	| '<='
	| '>='
	| '=='
	| '!='
	;

sumExpression
	: sumExpression sumOp term
	| term
	;

sumOp
	: '+'
	| '-'
	;

term
	: term mulOp unaryExpression
	| unaryExpression
	;

mulOp
	: '*'
	| '/'
	| '%'
	;

unaryExpression
	: unaryOp unaryExpression
	| factor
	;

unaryOp
	: '-'
	| '*'
	| '?'
	;

factor
	: immutable
	| mutable
	;

mutable
	: ID
	| mutable '[' expression ']'
	| '&' mutable
	;

immutable
	: '(' expression ')'
	| call
	| constant
	;

call
	: ID '(' args ')'
	;

args
	: argList
	| // empty
	;

argList
	: argList ',' expression
	| expression
	;

constant
	: 'true'
	| 'false'
	| NUMCONST
	| CHARCONST
	;

// ===============================================
// Tokens
// TODO: replace '...' with tokens (e.g. ';' => 'SEMICOLON: ';';')
// ===============================================

fragment NONDIGIT: [a-zA-Z_];
fragment DIGIT: [0-9];
LETDIG: DIGIT | NONDIGIT;

ID: NONDIGIT LETDIG*;
NUMCONST: DIGIT+;
CHARCONST: '"' ~('\r' | '\n' | '"')* '"';	//  '~' negates charsets

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