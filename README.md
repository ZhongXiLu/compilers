
# Compilers

###  Contributors

- Zhong-Xi Lu
- Jordan Parezys
    
### Optional features

Grammar:
- Break statement
- Comparison operators >=, <=, and !=
- Logical operators &&, ||

Optimisation:
- No code generation after `break`
- No code generation for unused variables
- No code generation for unused functions

### How to test and build

How to build and compile a c file (the AST and parse tree will be saved in the `output` directory as `.gv` and `.pdf` format):
```commandline
python3 build.py
python3 src/c2p.py c_prog.c
```

How to run all the tests:
```commandline
python3 test.py
```

### Test Files

- Correct Semantic (`src/tests/data/CorrectSemantic`)
- Correct Syntax (`src/tests/data/CorrectSyntax`)
- Correct Type (`src/tests/data/CorrectType`)
- Optimiser (`src/tests/data/Optimiser`)
- Semantic Errors (`src/tests/data/SemanticErrors`)
- Syntax Errors (`src/tests/data/SyntaxErrors`)
- Type Errors (`src/tests/data/TypeErrors`)
