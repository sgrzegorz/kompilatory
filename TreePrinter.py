from __future__ import print_function
import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.InstructionsOpt)
    def printTree(self, indent=0):
        if self.instructions:
            self.instructions.printTree()

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print("IF")
        self.booleanInParentheses.printTree(indent + 1)
        for i in range(indent):
            print("|  ", end='')
        print("THEN")
        self.instruction.printTree(indent + 1)

    @addToClass(AST.IfElse)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print("IF")
        self.booleanInParentheses.printTree(indent + 1)

        for i in range(indent):
            print("|  ", end='')
        print("THEN")
        self.instruction.printTree(indent + 1)
        for i in range(indent):
            print("|  ", end='')
        print("ELSE")
        self.else_instruction.printTree(indent + 1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print("PRINT")
        for i in self.print_expressions:
            # print("iiiiiiiiiiiii " + str(i))
            i.printTree(indent + 1)

    # =
    #     REF
    #     ID
    #         int
    #         int
    #     constant
    @addToClass(AST.AssignOperators)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print(self.oper)
        self.id.printTree(indent + 1)
        self.expression.printTree(indent + 1)

    @addToClass(AST.Assign)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print('=')
        self.id.printTree(indent + 1)
        self.expression.printTree(indent + 1)

    @addToClass(AST.AssignRef)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print('=')
        self.ref.printTree(indent + 1)

    @addToClass(AST.Ref)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print("REF")
        self.id.printTree(indent + 1)
        self.ind1.printTree(indent + 1)
        self.ind2.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print("WHILE")
        self.booleanInParentheses.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print("FOR")
        self.id.printTree(indent + 1)
        self.range.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print("RANGE")
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print("BREAK")

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print("CONTINUE")

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print("RETURN")
        if self.expr:
            self.expr.printTree(indent + 1)

    @addToClass(AST.Rows)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print("MATRIX")
        for i in self.rows:
            i.printTree(indent + 1)

    @addToClass(AST.Row)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print("VECTOR")
        for i in self.numbers:
            i.printTree(indent + 1)

    @addToClass(AST.MatrixFunctions)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print(self.func)
        self.expressions.printTree(indent + 1)

    @addToClass(AST.UMinusExpression)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print("UMINUS")
        self.expression.printTree(indent + 1)

    @addToClass(AST.Transposition)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print("TRANSPOSE")
        self.variable.printTree(indent + 1)

    # @addToClass(AST.PrintExpression)
    # def printTree(self, indent=0):
    #     for i in self.constans:
    #         i.printTree(indent + 1)

    @addToClass(AST.Expression)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print(self.oper)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.MultipleExpression)
    def printTree(self, indent=0):
        for e in self.exprs:
            e.printTree(indent)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print("PRINT")
        for i in self.print_expressions:
            # print("iiiiiiiiiiiii " + str(i))
            i.printTree(indent + 1)

    @addToClass(AST.BooleanExpression)  # TODO: is it necessary?
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print(self.oper)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Constant)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print(self.value)

    @addToClass(AST.Id)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end='')
        print(self.value)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        raise Exception("UNEXPECTED ERROR")
