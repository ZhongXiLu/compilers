# Compilers

###  Contributors

- Zhong-Xi Lu
- Jordan Parezys

### Progress (as of 22/04)

- TODO

### Test Files

- Correct Semantic (`src/tests/data/CorrectSemantic`)
    - `CorrectSemantic1.c`
    - `StdLib.c`

- Correct Syntax (`src/tests/data/CorrectSyntax`)
    - `Expressions.c`
    - `Functions.c`
    - `Statements.c`
    - `Variables.c`
    
- Correct Type (`src/tests/data/CorrectType`)
    - `CorrectType1.c`

- Semantic Errors (`src/tests/data/SemanticErrors`)
    - Undefined References
        - `NestedScope.c`
        - `UndefinedRefToFunc.c`
        - `UndefinedRefToVar.c`
    - Redefinitions
        - `RedefinitionFunc.c`
        - `RedefinitionVar.c`
    - Calling subscript on not an array
        - `SubscriptNotArray.c`
    - Too much params in call
        - `TooMuchParams.c`
        
- Syntax Errors (`src/tests/data/SyntaxErrors`)
    - Missing symbols
        - `MissingBracket.c`
        - `MissingSemiColon.c`
    - Wrong constructions
        - `WrongIfConstruction.c`
        - `WrongKeyword.c`
        
- Type Errors (`src/tests/data/TypeErrors`)
    - Assign wrong type to variable
        - `AssignIntToChar.c`
        - `AssignIntToString.c`
        - `AssignStringToInt.c`
        - `AssignWrongArrayElementToChar.c`
        - `AssignWrongCallToInt.c`
    - Type operations errors
        - `IntPlusString.c`
        - `WrongNestedExpressions.c`
    - Call type errors
        - `WrongTypeOfParams.c`
        - `WrongTypeOfParams2.c`