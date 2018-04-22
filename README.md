
# Compilers

###  Contributors

- Zhong-Xi Lu
- Jordan Parezys

### Progress (as of 22/04)

#### Implemented features
- Basic grammar completed
- Reporting lexical errors
- Reporting syntactical errors
- Constructing and visualising AST
    - AST Classes/Nodes in use
- Reporting semantical errors (roughly done)
    - Symbol table in use
    
#### Optional features
- Break statement
- Comparison operators >=, <=, and !=
- Logical operators &&, ||
- Some type conversions
    - Double to int
    - *bool* to int

### How to test and build

How to build:
```commandline
python3 build.py
python3 src/main.cpp c_prog
```
Note that during the execution, the AST will be shown by default.
The AST and parse tree will be saved in `output` as `.gv` and `.pdf` format.

How to test:
```commandline
python3 test.py
```

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
        - `DeclWithNoDef.c`
        - `DefWithWrongDecl.c`
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