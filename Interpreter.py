
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys
import numpy as np

sys.setrecursionlimit(10000)

class Interpreter(object):
    def __init__(self):  # memory name
        self.memory_stack = MemoryStack()

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
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        node.instructions.accept(self)


    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)


    @when(AST.If)
    def visit(self, node):
        node.booleanInParentheses.accept(self)
        node.instruction.accept(self)
        pass

    @when(AST.IfElse)
    def visit(self, node):
        node.booleanInParentheses.accept(self)
        node.instruction.accept(self)
        node.else_instruction.accept(self)
        pass

    @when(AST.For)
    def visit(self, node):
        self.memory_stack.push(Memory("For"))
        node.id.accept(self)
        node.range.accept(self)
        node.instruction.accept(self)
        self.memory_stack.pop()


    @when(AST.Range)
    def visit(self, node):
        node.start.accept(self)
        node.end.accept(self)
        pass

    @when(AST.While)
    def visit(self, node):
        self.memory_stack.push(Memory("While"))
        node.booleanInParentheses.accept(self)
        node.instruction.accept(self)
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
        pass

    @when(AST.AssignOperators)
    def visit(self, node):
        node.id.accept(self)
        node.expression.accept(self)
        pass

    @when(AST.Assign)
    def visit(self, node):
        node.id.accept(self)
        node.expression.accept(self)
        pass

    @when(AST.AssignRef)
    def visit(self, node):
        node.expression.accept(self)
        pass

    @when(AST.Ref)
    def visit(self, node):
        node.ind1.accept(self)
        node.ind2.accept(self)
        pass

    @when(AST.Expression)
    def visit(self, node):
        node.left.accept(self)
        node.right.accept(self)
        pass

    @when(AST.MultipleExpression)
    def visit(self, node):
        for e in node.exprs:
            e.accept(self)
        pass

    @when(AST.BooleanExpression)
    def visit(self, node):
        node.left.accept(self)
        node.right.accept(self)
        pass

    @when(AST.UMinusExpression)
    def visit(self, node):
        pass

    @when(AST.Transposition)
    def visit(self, node):
        return (-1)*node.expression.accept(self)


    @when(AST.Rows)
    def visit(self, node):

        rows =[]
        for row in node.rows:
            rows.append(row.accept(self))
        pass

    @when(AST.Row)
    def visit(self, node):
        for number in node.numbers:
            number.accept(self)
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
