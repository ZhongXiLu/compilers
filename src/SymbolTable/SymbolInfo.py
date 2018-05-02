

class SymbolInfo:

    def __init__(self, type):
        self.type = type
        self.used = False   # Check if this symbol is ever used
        self.address = 0    # Used for code generation (= address of the symbol)


class VarInfo(SymbolInfo):

    def __init__(self, type):
        super().__init__(type)


class FunctionInfo(SymbolInfo):

    def __init__(self, returnType, paramTypes, isDecl=False):
        super().__init__(returnType)
        self.paramTypes = paramTypes
        self.isDecl = isDecl


class ArrayInfo(SymbolInfo):

    def __init__(self, type, size):
        super().__init__(type)
        self.size = size
