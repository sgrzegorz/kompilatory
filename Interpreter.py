
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
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


    @on('node')
    def visit(self, node):
        pass

    # @when(AST.BinOp)
    # def visit(self, node):
    #     r1 = node.left.accept(self)
    #     r2 = node.right.accept(self)
    #     # try sth smarter than:
    #     # if(node.op=='+') return r1+r2
    #     # elsif(node.op=='-') ...
    #     # but do not use python eval

    # @when(AST.Assignment)
    # def visit(self, node):
    # #
    # #
    #
    # # simplistic while loop interpretation
    # @when(AST.WhileInstr)
    # def visit(self, node):
    #     r = None
    #     while node.cond.accept(self):
    #         r = node.body.accept(self)
    #     return r
    #

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

        name =node.id.accept(self)
        (start, end) = node.range.accept(self)

        for i in range(start,end): #TODO check range
            try:
                self.memory_stack.insert(name,i)
                node.instruction.accept(self)
                self.memory_stack.delete(name,i)
            except ReturnValueException: #TODO return check
                return
            except ContinueException:
                continue
            except BreakException:
                break

        self.memory_stack.pop()


    @when(AST.Range)
    def visit(self, node):
        start =node.start.accept(self)
        end =node.end.accept(self)
        return (start,end)
        pass

    @when(AST.While)
    def visit(self, node):
        self.memory_stack.push(Memory("While"))


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
        string =''
        for expression in node.print_expressions:
            string+=expression.accept(self)
        print(string)

    @when(AST.AssignOperators) # x += , -=, *=, /=
    def visit(self, node):
        name = node.id.accept(self)
        left = self.memory_stack.get(name)
        right = node.expression.accept(self)
        result = self.operators[node.oper](left,right)
        self.memory_stack.set(name,result)
        pass

    @when(AST.Assign)
    def visit(self, node):
        name = node.id.accept(self)
        val=node.expression.accept(self)
        self.memory_stack.insert(name,val)
        pass

    @when(AST.AssignRef)
    def visit(self, node):
        (ind1,ind2) = node.ref.accept(self)
        expression =node.expression.accept(self)
        matrix = self.memory_stack.get(node.ref.name)

        if matrix!=None:
            matrix[ind1,ind2] = expression
        pass

    @when(AST.Ref)
    def visit(self, node):
        ind1 = node.ind1.accept(self)
        ind2 = node.ind2.accept(self)
        return (ind1,ind2)

    @when(AST.Expression)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        left,right = [ self.getValueWhenID(i) for i in [left,right]]
        return self.operators[node.oper](left,right) #TODO matrix multiplication bedzie inaczej

    @when(AST.MultipleExpression)
    def visit(self, node):
        t = []
        for expr in node.exprs:
            t.append(expr.accept(self))
        return t


    def getValueWhenID(self,val):
        if isinstance(val, str):
            val = self.memory_stack.get(val)
            if val is None:
                print('This shouldnt be printed')
        return val

    @when(AST.BooleanExpression)
    def visit(self, node):
        left =node.left.accept(self)
        right =node.right.accept(self)
        left,right = [ self.getValueWhenID(i) for i in [left,right]]

        return self.operators[node.oper](left,right)
        pass

    @when(AST.UMinusExpression)
    def visit(self, node):
        return (-1)*node.expression.accept(self)

    @when(AST.Transposition)
    def visit(self, node):
        matrix = node.expression.accept(self)
        return np.transpose(matrix)
        pass

    @when(AST.Rows)
    def visit(self, node):

        rows =[]
        for row in node.rows:
            rows.append(row.accept(self))
        matrix = np.vstack(rows)
        return matrix

    @when(AST.Row)
    def visit(self, node):
        row =[]
        for number in node.numbers:
            row.append(number.accept(self))
        return np.array(row)
        pass

    @when(AST.MatrixFunctions)
    def visit(self, node):
        node.expressions.accept(self)
        return np.array()

    @when(AST.Constant)
    def visit(self, node):
        return node.value

    @when(AST.Id)
    def visit(self, node):
        return node.value
        pass
