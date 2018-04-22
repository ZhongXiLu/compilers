

class VarInfo:

    def __init__(self, type):
        self.type = type
        # self.declLineNr
        # self.refLineNrs


class FunctionInfo:

    def __init__(self, returnType, paramTypes, isDecl=False):
        self.returnType = returnType
        self.paramTypes = paramTypes
        self.isDecl = isDecl


class ArrayInfo:

    def __init__(self, type, size):
        self.type = type
        self.size = size


class Scope:

    def __init__(self):
        self.table = {}
        self.children = []
        self.parent = None

    def newScope(self):
        newScope = Scope()
        newScope.parent = self
        self.children.append(newScope)
        return newScope

    def endScope(self):
        return self.parent


class SymbolTable:
    """
        SymbolTable:
        - inspiration: http://labouseur.com/courses/compilers/AST-and-Symbol-Table.pdf
        - Tree structure with scopes as nodes
        - The current scope is indicated with the currentScope pointer
    """

    def __init__(self):
        self.scope = Scope()    # Root (most outer scope)
        self.currentScope = self.scope

    def newScope(self):
        self.currentScope = self.currentScope.newScope()

    def endScope(self):
        self.currentScope = self.currentScope.endScope()

    def getSymbol(self, symbol):
        currentScopeSearch = self.currentScope

        # Search in current scope
        try:
            symbolInfo = currentScopeSearch.table[symbol]
            return symbolInfo
        except:
            currentScopeSearch = currentScopeSearch.parent

        # Search in outer scopes
        while currentScopeSearch is not None:
            try:
                symbolInfo = currentScopeSearch.table[symbol]
                return symbolInfo
            except:
                currentScopeSearch = currentScopeSearch.parent
        return None

    def getSymbolInCurrentScope(self, symbol):
        # Search in current scope
        try:
            symbolInfo = self.currentScope.table[symbol]
            return symbolInfo
        except:
            return None

    def addSymbol(self, symbol, symbolInfo):
        self.currentScope.table[symbol] = symbolInfo
