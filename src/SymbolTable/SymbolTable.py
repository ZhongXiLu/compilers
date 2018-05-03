

class Scope:

    def __init__(self):
        self.table = {}
        self.currentChild = 0
        self.children = []
        self.parent = None

    def newScope(self):
        newScope = Scope()
        newScope.parent = self
        self.children.append(newScope)
        return newScope

    def endScope(self):
        return self.parent

    # Used for traversing
    def getNextScope(self):
        self.currentChild += 1
        return self.children[self.currentChild-1]

    # Reset the child pointers (used when traversing the symbol table again)
    def reset(self):
        self.currentChild = 0
        for child in self.children:
            child.reset()


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

    # Reset the child pointers (used when traversing the symbol table again)
    def reset(self):
        self.currentScope = self.scope
        self.currentScope.reset()
