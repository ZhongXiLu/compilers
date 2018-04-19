# Compilers

###  Contributors

- Zhong-Xi Lu
- Jordan Parezys

### Progress (as of 22/04)

- TODO

### Test Files

- Semantic Errors (`src/tests/data/SemanticErrors`):
    - Undefined References:
        - `NestedScope.c`
        - `UndefinedRefToFunc`
        - `UndefinedRefToVar`
    - Redefinitions:
        - `RedefinitionFunc.c`
        - `RedefinitionVar.c`
    - Calling subscript on not an array
        - `SubscriptNotArray.c`
        
- Syntax Errors (`src/tests/data/SyntaxErrors`)
    - Missing symbols
        - `MissingBracket.c`
        - `MissingSemiColon.c`
    - Wrong constructions
        - `WrongIfConstruction.c`
        - `WrongKeyword.c`
