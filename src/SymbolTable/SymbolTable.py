

class Scope:

    def __init__(self):
        self.table = {}
        self.currentChild = 0   # Used for traversing
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
