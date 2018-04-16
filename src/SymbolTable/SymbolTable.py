

# TODO: split in variable and function info?
class SymbolInfo:

    def __init__(self, type):
        self.type = type


class SymbolTable:
    """
        SymbolTable:
        - list of dicts, one dict for each scope
        - the first (and last added) one, is the current scope
    """

    def __init__(self):
        self.scopes = []

    def newScope(self):
        self.scopes.insert(0, {})

    def endScope(self):
        self.scopes.pop(0)

    def getSymbol(self, symbol):
        for scope in self.scopes:
            try:
                symbolInfo = scope[symbol]
                return symbolInfo
            except:
                pass
        return None

    def addSymbol(self, symbol, symbolInfo):
        self.scopes[0][symbol] = symbolInfo
