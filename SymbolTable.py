#!/usr/bin/python
class Symbol:
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class VariableSymbol(Symbol):
    def __init__(self, name=None, type=None, dim1=None, dim2=None):
        super().__init__(name, type)
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

    def remember_parameters(self, name=None, type=None, dim1=None, dim2=None):
        if (type != None): self.type = type
        if (name != None): self.name = name
        if (dim1 != None): self.dim1 = dim1
        if (dim2 != None): self.dim2 = dim2

    def remember_dimensions(self, name=None, dim1=None, dim2=None):
        if (name != None): self.name = name
        if (dim1 != None): self.dim1 = dim1
        if (dim2 != None): self.dim2 = dim2

    # __repr__ = __str__


# right_type = typeof(b + c)
# if right_type == 'unknown':
#     error
# else:
#     save 'a' to variable symbol table - initialized with value(b+c)

# class MatrixSymbol(Symbol):
#     def __init__(self, name, type,dim1=None,dim2=None):
#         super().__init__(name, type)
#         self.dim1 = dim1
#         self.dim2 = dim2


# def __str__(self):
#     return "<{class_name}(name='{name}', type='{type}')>".format(
#         class_name=self.__class__.__name__,
#         name = self.name,
#         type = self.type,
#         dim1 = self.dim1,
#         dim2 = self.dim2
#     )
# __repr__ = __str__


class SymbolTable(object):

    def __init__(self, parent, name):  # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.scope = 0
        self.nesting = 0
        self.recent_id = None
        # {'x' : VariableSymbol('x','int'}
        # {Node19bfdifa1 : MatrixSymbol('y','matrix', dimensions=10) #matrix 10x10 TODO: save the whole matrix, not just dimensions
        self.symbols = {}

    #

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol
        symbol.name = name
        self.recent_id = name

    #
    #     # b = a+5
    # # b -> VariableSymbol()
    # a = c + 4; # a = VariableSybol()
    # b = a + 5;

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

