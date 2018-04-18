
// based on: http://marvin.cs.uidaho.edu/Teaching/CS445/c-Grammar.pdf

grammar C;

// ===============================================
// Main Program Rules
// ===============================================

prog: includes declarationList;

declarationList
	: declaration
	| declarationList declaration
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
	: '#' 'include' '<' Library '>'
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
	: Id
	| Id '=' simpleExpression
	| Id '[' IntConst ']'
	| Id '[' IntConst ']' '=' '{' arrayInitializeList '}'
	;

arrayInitializeList
    : arrayInitializeList ',' simpleExpression
    | simpleExpression
    ;

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
	: functionTypeSpecifier Id '(' params ')' compoundStmt
	// | ID '(' params ')' compoundStmt 	// TODO: is this correct C ?
	;

functionTypeSpecifier
    : 'void'
    | typeSpecifier
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
	: typeSpecifier Id
	;

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
	: '{' '}'
	| '{' statementList '}'
	| '{' localDeclarations '}'
	| '{' localDeclarations statementList '}'
	;

localDeclarations
	: varDeclaration
	| localDeclarations varDeclaration
	;

statementList
	: statement
	| statementList statement
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
	: '(' expression ')'
	| mutable '=' expression
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
//	| '%'
	;

unaryExpression
	: unaryOp unaryExpression
	| factor
	;

unaryOp
	: '-'
	;

factor
	: immutable
	| mutable
	;

mutable
	: Id
	| mutable '[' expression ']'
	;

immutable
	: '(' expression ')'
	| call
	| constant
	;

call
	: Id '(' args ')'
	;

args
	: args ',' expression
	| expression
	| // empty
	;

// TODO: 'true'/'false' correct C ?
constant
	: 'true'
	| 'false'
	| IntConst
	| DoubleConst
	| CharConst
	;

// ===============================================
// Tokens
// TODO: replace '...' with tokens (e.g. ';' => 'SEMICOLON: ';';') ?
// ===============================================

// 'fragment': "You can also define rules that are not tokens but rather aid in the recognition of tokens.
//              These fragment rules do not result in tokens visible to the parser"

fragment NonDigit: [a-zA-Z_];
fragment Digit: [0-9];
fragment LetDig: Digit | NonDigit;

Id: NonDigit LetDig*;
IntConst: Digit+;
DoubleConst: (Digit* '.' Digit+) | (Digit+ '.' Digit*);   // TODO: support more (e.g. 1e10)?
CharConst: '"' ~('\r' | '\n' | '"')* '"';	//  '~' negates charsets
Library: (Id | Id '.' Id);

// ===============================================
// Comments & Other
// ===============================================

Whitespace
	: [ \t]+
		-> skip
	;

Newline
	: ('\r' '\n'? | '\n')
		-> skip
	;

BlockComment
	: '/*' .*? '*/'
		-> skip
	;

LineComment
	: '//' ~[\r\n]*
		-> skip
	;