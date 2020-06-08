class Symbol:
    def __init__(self, name, type=None, val=None):
        self.name = name
        self.type = type
        self.val = val


class MatrixSymbol(Symbol):
    def __init__(self, name=None, type=None, val=None, dim1=None, dim2=None):
        super().__init__(name, type, val)
        self.dim1 = dim1
        self.dim2 = dim2


def __str__(self):
    return "<{class_name}(name='{name}', type='{type}')>".format(
        class_name=self.__class__.__name__,
        name=self.name,
        type=self.type,
        dim1=self.dim1,
        dim2=self.dim2
    )


class SymbolTable(object):

    def __init__(self, parent, name):  # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.scope = 0
        self.nesting = 0
        # {'x' : VariableSymbol('x','int'}
        # {Node19bfdifa1 : MatrixSymbol('y','matrix', dimensions=10) #matrix 10x10 TODO: save the whole matrix, not just dimensions
        self.symbols = {}

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol
        symbol.name = name

    def get(self, name):  # get variable symbol or fundef from <name> entry
        return self.symbols[name]

    #

    def getParentScope(self):
        return self.parent

    #

    def pushScope(self, name):
        self.scope += 1

    #

    def popScope(self):
        self.scope -= 1

    def pushNesting(self):
        self.nesting += 1

    def popNesting(self):
        self.nesting -= 1
    #
