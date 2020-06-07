import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys
import numpy as np
import operator

sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):  # memory name
        self.memory_stack = MemoryStack()
        self.operators = dict()
        self.operators['*'] = operator.mul
        self.operators['/'] = operator.truediv
        self.operators['+'] = operator.add
        self.operators['-'] = operator.sub
        self.operators['.*'] = operator.mul
        self.operators['./'] = operator.truediv
        self.operators['.+'] = operator.add
        self.operators['.-'] = operator.sub
        self.operators['>'] = operator.gt
        self.operators['<'] = operator.lt
        self.operators['>='] = operator.ge
        self.operators['<='] = operator.le
        self.operators['=='] = operator.eq
        self.operators['!='] = operator.ne
        self.operators['+='] = operator.add
        self.operators['-='] = operator.sub
        self.operators['/='] = operator.truediv
        self.operators['*='] = operator.mul

    @on('node')
    def visit(self, node):
        pass

    @when(AST.InstructionsOpt)
    def visit(self, node):
        node.instructions.accept(self)

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(AST.If)
    def visit(self, node):
        if node.booleanInParentheses.accept(self):
            node.instruction.accept(self)

    @when(AST.IfElse)
    def visit(self, node):
        if node.booleanInParentheses.accept(self):
            node.instruction.accept(self)
        else:
            node.else_instruction.accept(self)
        pass

    @when(AST.For)
    def visit(self, node):
        self.memory_stack.push(Memory("For"))

        (start, end) = node.range.accept(self)

        if not self.memory_stack.set(node.id.name, start):
            self.memory_stack.insert(node.id.name, start)

        while self.memory_stack.get(node.id.name) < end:
            try:
                node.instruction.accept(self)

                self.memory_stack.set(node.id.name, self.memory_stack.get(node.id.name) + 1)  # i+=1
            except ReturnValueException:  # TODO return check
                return
            except ContinueException:
                self.memory_stack.set(node.id.name, self.memory_stack.get(node.id.name) + 1)  # i+=1
                continue
            except BreakException:
                break

        self.memory_stack.pop()

    @when(AST.Range)
    def visit(self, node):
        start = node.start.accept(self)
        end = node.end.accept(self)
        return (start, end)
        pass

    @when(AST.While)
    def visit(self, node):
        self.memory_stack.push(Memory("While"))  ## lekkie uproszczenie powinno być wewnątrz while

        while node.booleanInParentheses.accept(self):

            try:
                node.instruction.accept(self)
            except ReturnValueException:  # TODO return check
                return
            except ContinueException:
                continue
            except BreakException:
                break

        self.memory_stack.pop()

    @when(AST.Break)
    def visit(self, node):
        raise BreakException
        pass

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException
        pass

    @when(AST.Return)
    def visit(self, node):
        raise ReturnValueException
        pass

    @when(AST.Print)
    def visit(self, node):
        printExpressions = node.multiple_expression.accept(self)
        for expression in printExpressions:
            print(expression, end=" ")
        print()

    @when(AST.AssignOperators)  # x += , -=, *=, /=
    def visit(self, node):
        # name = node.id.accept(self)
        left = self.memory_stack.get(node.id.name)
        right = node.expression.accept(self)

        if node.oper == '*=' and isinstance(left, np.ndarray) and isinstance(right, np.ndarray):
            result = np.matmul(left, right)
        else:
            result = self.operators[node.oper](left, right)
        self.memory_stack.set(node.id.name, result)
        pass

    @when(AST.Assign)
    def visit(self, node):
        #  name = node.id.accept(self)
        val = node.expression.accept(self)
        # k = 2; for such situation im working on one global k
        # while (k > 0) {
        # k = k - 1;
        # }
        if not self.memory_stack.set(node.id.name, val):
            self.memory_stack.insert(node.id.name, val)
        pass

    @when(AST.AssignRef)
    def visit(self, node):
        (ind1, ind2) = node.ref.accept(self)
        expression = node.expression.accept(self)
        matrix = self.memory_stack.get(node.ref.id.name)

        if matrix is not None:
            matrix[ind1 - 1, ind2 - 1] = expression  # -1 because array indexation from 1 to N
        pass

    @when(AST.Ref)
    def visit(self, node):
        ind1 = node.ind1.accept(self)
        ind2 = node.ind2.accept(self)
        return (ind1, ind2)

    @when(AST.Expression)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if node.oper == '*' and isinstance(left, np.ndarray) and isinstance(right, np.ndarray):
            return np.matmul(left, right)
        return self.operators[node.oper](left, right)  # TODO matrix multiplication bedzie inaczej

    @when(AST.MultipleExpression)
    def visit(self, node):
        t = []
        for expr in node.exprs:
            t.append(expr.accept(self))
        return t

    @when(AST.BooleanExpression)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)

        if node.oper in ('!=', '==') and isinstance(left, np.ndarray) and isinstance(right, np.ndarray):
            return np.array_equal(left, right)

        return self.operators[node.oper](left, right)
        pass

    @when(AST.UMinusExpression)
    def visit(self, node):
        return (-1) * node.expression.accept(self)

    @when(AST.Transposition)
    def visit(self, node):
        matrix = node.expression.accept(self)
        return np.transpose(matrix)
        pass

    @when(AST.Rows)
    def visit(self, node):

        rows = []
        for row in node.rows:
            rows.append(row.accept(self))
        matrix = np.vstack(rows)
        return matrix

    @when(AST.Row)
    def visit(self, node):
        row = []
        for number in node.numbers:
            row.append(number.accept(self))

        return np.array(row)
        pass

    @when(AST.MatrixFunctions)
    def visit(self, node):
        dims = node.expressions.accept(self)
        if len(dims) == 1:
            dims.append(dims[0])
        dims = tuple(dims)

        if node.func == 'ones':
            return np.ones(dims)

        elif node.func == 'zeros':
            return np.zeros(dims)
        elif node.func == 'eye':
            return np.eye(dims[0])  # todo: dim is always a number in this case

    @when(AST.MatixFunctionsExpression)
    def visit(self, node):
        dims = []
        for i in node.exprs:
            dims.append(i.accept(self))
        return dims

    @when(AST.Constant)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value[1:-1]

    @when(AST.Id)
    def visit(self, node):
        return self.memory_stack.get(node.name)
        pass
