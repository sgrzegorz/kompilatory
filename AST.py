
class Node(object):
    # def __init__(self, children):
    #     self.children = children
    def __init__( self , *children ) :
        self.line = 0
        if not children : self.children = []
        elif hasattr( children , '__len__' ) :
            self.children = children
        else:
            self.children = [ children ]

    def accept(self, visitor): #function for lab5
        return visitor.visit(self)

class InstructionsOpt(Node):
    def __init__(self, instructions=None):
        # super().__init__(instructions)
        self.instructions = instructions

class Instructions(Node):
    def __init__(self, instruction):
        # super().__init__(instruction)
        self.instructions = [instruction]
    def append(self, instruction):
        self.instructions.append(instruction)

class If(Node):
    def __init__(self, booleanInParentheses, instruction):
        # super().__init__(booleanInParentheses,instruction)
        self.booleanInParentheses = booleanInParentheses
        self.instruction = instruction

class IfElse(Node):
    def __init__(self, booleanInParentheses, instruction, else_instruction):
        # super().__init__(booleanInParentheses,instruction,else_instruction)
        self.booleanInParentheses = booleanInParentheses
        self.instruction = instruction
        self.else_instruction = else_instruction

class For(Node):
    def __init__(self, id, range, instruction):
        # super.__init__(id,range,instruction)
        self.id = id
        self.range = range
        self.instruction = instruction

class Range(Node):
    def __init__(self, start, end):
        # super().__init__(start,end)
        self.start = start
        self.end = end

class While(Node):
    def __init__(self, booleanInParentheses, instruction):
        # super().__init__(booleanInParentheses,instruction)
        self.booleanInParentheses = booleanInParentheses
        self.instruction = instruction

class Break(Node):
    def __init__(self):
        # super.__init__()
        pass

class Continue(Node):
    def __init__(self):
        # super.__init__()
        pass

class Return(Node):
    def __init__(self, expr = None):
        # super.__init__(expr)
        self.expr = expr

class Print(Node):
    def __init__(self, multiple_expression):
        self.multiple_expression = multiple_expression
    # def append(self, print_expression):
    #     self.print_expressions.append(print_expression)

class AssignOperators(Node):
    def __init__(self, oper, id, expression):
        self.oper = oper
        self.id = id
        self.expression = expression

class Assign(Node):
    def __init__(self, id, expression):
        self.id = id
        self.expression = expression

class AssignRef(Node):
    def __init__(self, ref, expression):
        self.ref = ref
        self.expression = expression

class Ref(Node):
    def __init__(self, id, ind1, ind2):
        self.id = id
        self.ind1 = ind1
        self.ind2 = ind2

class Expression(Node):
    def __init__(self, oper, left, right):
        self.oper = oper
        self.left = left
        self.right = right

class MultipleExpression(Node):
    def __init__(self, expr):
        self.exprs = [expr]
    def append(self, expr):
        self.exprs.append(expr)

class MatixFunctionsExpression(Node):
    def __init__(self, expr):
        self.exprs = [expr]
    def append(self, expr):
        self.exprs.append(expr)

class BooleanExpression(Node):
    def __init__(self, oper, left, right):
        self.oper = oper
        self.left = left
        self.right = right

class UMinusExpression(Node):
    def __init__(self, expression):
        self.expression = expression

class Transposition(Node):
    def __init__(self, expression):
        self.expression = expression

# class Matrix(Node):
#     def __init__(self, rows):
#         self.rows = rows

class Rows(Node):
    def __init__(self, row):
        self.rows = [row]
    def append(self, row):
        self.rows.append(row)

class Row(Node):
    def __init__(self, number):
        self.numbers = [number]
    def append(self, number):
        self.numbers.append(number)

class MatrixFunctions(Node):
    def __init__(self, func, expressions):
        self.func = func
        self.expressions = expressions

class Constant(Node):
    def __init__(self, value):
        self.value = value

class String(Node):
    def __init__(self, value):
        self.value = value

class Id(Node):
    def __init__(self, value):
        self.value = value

class Error(Node):
    def __init__(self):
        pass
