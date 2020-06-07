#!/usr/bin/python
import inspect

import AST
from SemanticRules import SemanticRules
from SymbolTable import *

verbose = False


class NodeVisitor(object):
    def __init__(self):
        self.semantic_rules = SemanticRules()
        self.symbol_table = SymbolTable(None, 'Program')
        self.error = False
        self.shouldThrowUndeclaredIdError = True

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            nodeChildren = node.__dict__.values()
            for child in nodeChildren:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    def handle_error(self, message):
        self.error = True
        print(message)

    def printFunctionName(self):
        print(inspect.stack()[1][3])


class TypeChecker(NodeVisitor):

    def visit_InstructionsOpt(self, node):
        if (verbose): self.printFunctionName()
        self.visit(node.instructions)

    def visit_Instructions(self, node):
        if (verbose): self.printFunctionName()
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_If(self, node):
        if (verbose): self.printFunctionName()
        self.symbol_table.pushScope('if')

        self.visit(node.booleanInParentheses)
        self.visit(node.instruction)

        self.symbol_table.popScope()

    def visit_IfElse(self, node):
        if (verbose): self.printFunctionName()
        self.symbol_table.pushScope('if')
        self.visit(node.booleanInParentheses)
        self.visit(node.instruction)
        self.symbol_table.popScope()

        self.symbol_table.pushScope('else')
        self.visit(node.else_instruction)
        self.symbol_table.popScope()

    def visit_For(self, node):
        if (verbose): self.printFunctionName()
        self.symbol_table.pushNesting()
        self.symbol_table.pushScope('for')

        self.symbol_table.put(node.id.name, Symbol(name=node.id.name, type='int'))
        self.visit(node.id)
        self.visit(node.range)
        self.visit(node.instruction)

        self.symbol_table.popScope()
        self.symbol_table.popNesting()

    def visit_Range(self, node):
        if (verbose): self.printFunctionName()
        start_type = self.visit(node.start)
        end_type = self.visit(node.end)
        if start_type == 'unknown' or end_type == 'unknown':
            return 'unknown'
        elif start_type != 'int' or end_type != 'int':
            self.handle_error('Line {}: Range of unsupported types: {} and {}'.format(node.line, start_type, end_type))
            return 'unknown'
        return 'int'  # TODO: think it over

    def visit_While(self, node):
        if (verbose): self.printFunctionName()
        self.symbol_table.pushNesting()
        self.symbol_table.pushScope('while')

        self.visit(node.booleanInParentheses)
        self.visit(node.instruction)

        self.symbol_table.popScope()
        self.symbol_table.popNesting()

    def visit_Break(self, node):
        if (verbose): self.printFunctionName()
        if (self.symbol_table.nesting == 0):
            self.handle_error('Line {}: Trying to break from outside of a loop'.format(node.line))

    def visit_Continue(self, node):
        if (verbose): self.printFunctionName()
        if (self.symbol_table.nesting == 0):
            self.handle_error("Line {}: Trying to call continue from outside of a loop".format(node.line))

    def visit_Return(self, node):
        if (verbose): self.printFunctionName()
        self.visit(node.expr)

    def visit_Assign(self, node):
        if (verbose): self.printFunctionName()

        right_type = self.visit(node.expression)

        if right_type == 'matrix':
            matrix = node.expression

            if isinstance(matrix, AST.MatrixFunctions):  # zeros(a,b,c) TODO: modify matrices to be multiple-dim
                matrix_func_dims = []
                for expr in matrix.expressions.exprs:
                    if isinstance(expr, AST.Id):
                        if self.visit(expr) == 'unknown':
                            return 'unknown'

                        value = self.symbol_table.get(expr.name)
                        matrix_func_dims.append(value)
                    else:
                        matrix_func_dims.append(expr.value)

                if len(matrix.expressions.exprs) == 1:  # zeros(2) <=> zeros(2,2)
                    dim1 = matrix_func_dims[0]
                    dim2 = dim1
                if len(matrix.expressions.exprs) == 2:  # zeros(3,1), zeros(2,2)
                    dim1 = matrix_func_dims[0]
                    dim2 = matrix_func_dims[1]
            elif isinstance(matrix, AST.Expression):  # it's a matrix expression
                dim1 = self.symbol_table.get(matrix.left.name).dim1  # might be done differently as well
                dim2 = self.symbol_table.get(matrix.left.name).dim2
            else:  # it's a Rows object
                dim1, dim2 = self.get_matrix_dimensions(matrix)
            symbol = VariableSymbol(name=node.id.name, type=right_type, dim1=dim1, dim2=dim2)  # TODO: check
        else:
            symbol = Symbol(name=node.id.name, type=right_type)
        self.symbol_table.put(node.id.name, symbol)
        return right_type

    def visit_AssignOperators(self, node):  # x += , -=, *=, /=
        if (verbose): self.printFunctionName()

        left_type = self.visit(node.id)
        right_type = self.visit(node.expression)

        if left_type == 'unknown' or right_type == 'unknown':
            return 'unknown'

        left = self.symbol_table.get(node.id.name)
        return_type = self.semantic_rules.types[node.oper][left_type][right_type]

        if return_type == 'unknown':
            self.handle_error('Line {}: Unsupported operation between {} {}'.format(node.line, left.type, right_type))
            return 'unknown'

        if left_type == 'matrix' and right_type == 'matrix':
            if isinstance(node.expression, AST.Id):
                right_matrix = self.symbol_table.get(node.expression.name)
                right_dim1 = right_matrix.dim1
                right_dim2 = right_matrix.dim2
            elif isinstance(node.expression, AST.Rows):
                right_matrix = node.expression
                right_dim1, right_dim2 = self.get_matrix_dimensions(right_matrix)
            elif isinstance(node.expression, AST.MatrixFunctions):
                self.handle_error('Line {}: We reject expressions of form a += ones(2) '.format(node.line))
                return 'unknown'
            else:
                print('it should be impossible')
                return 'unknown'  # it should be impossible

            if node.oper == '*=':
                if left.dim2 != right_dim1:
                    self.handle_error(
                        'Line {}: Matrices dimensions do not match on matrix multiplication'.format(node.line))
                    return 'unknown'
                return return_type

            if left.dim1 != right_dim1 or left.dim2 != right_dim2:
                self.handle_error('Line {}: Matrices dimensions do not match'.format(node.line))
                return 'unknown'
        return return_type

    def get_matrix_dimensions(self, matrix):
        # it must be matrix of correct dimensions - otherwise
        # node.expression wouldn't have returned that matrix type is 'matrix'
        return len(matrix.rows), len(matrix.rows[0].numbers)

    def visit_AssignRef(self, node):  # x[1,2] = 6
        if (verbose): self.printFunctionName()
        self.visit(node.ref)
        self.visit(node.expression)

    def visit_Ref(self, node):  # x[1,2]
        if (verbose): self.printFunctionName()
        # node_name = self.visit(node.id)
        try:
            symbol = self.symbol_table.get(node.id.name)
        except KeyError:
            self.handle_error('Line {}: {} is used but not declared'.format(node.line, node.id.name))
            return 'unknown'
        if symbol.type == 'unknown':
            return 'unknown'
        elif symbol.type != 'matrix':
            self.handle_error('Line {}: Reference to: {}'.format(node.line, symbol.type))
            return 'unknown'

        ind1_type = self.visit(node.ind1)
        ind2_type = self.visit(node.ind2)

        for t in {ind1_type, ind2_type}:
            if t != 'unknown' and t != 'int':  # TODO: sprawdzić, czy jest niesiony
                self.handle_error('Line {}: index is not integer'.format(node.line))
                return 'unknown'

        if node.ind1.value <= 0 or node.ind2.value <= 0 or node.ind1.value > symbol.dim1 or node.ind2.value > symbol.dim2:
            self.handle_error(
                'Line {}: [{},{}] incorrect dimension reference, array indexation starts from 1'.format(node.line,
                                                                                                        node.ind1.value,
                                                                                                        node.ind2.value))
            return 'unknown'

    def visit_Expression(self, node):
        if (verbose): self.printFunctionName()
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type == 'unknown' or right_type == 'unknown':
            return 'unknown'

        if left_type == 'matrix' and right_type == 'matrix':
            left_dim1 = self.symbol_table.get(node.left.name).dim1
            left_dim2 = self.symbol_table.get(node.left.name).dim2  # FIXME
            right_dim1 = self.symbol_table.get(node.right.name).dim1
            right_dim2 = self.symbol_table.get(node.right.name).dim2

            if node.oper == '*' and left_dim2 == right_dim1:
                return 'matrix'
            if left_dim1 != right_dim1 or left_dim2 != right_dim2:
                self.handle_error(
                    'Line {}: Unsupported operation between matrices of different dimensions'.format(node.line))
                return 'unknown'

        return_type = self.semantic_rules.types[node.oper][left_type][right_type]
        if return_type == 'unknown':
            self.handle_error(
                'Line {}: Operation {} unsupported between types: {} and {}'.format(node.line, node.oper, left_type,
                                                                                    right_type))
            return 'unknown'
        return return_type

    def visit_MatrixFunctions(self, node):
        if (verbose): self.printFunctionName()

        if node.func == 'eye' and len(node.expressions.exprs) != 1:
            self.handle_error(self.get_error_message_for_matrix_fun(
                node) + " eye must be square, we allow only eye(5)")
            return 'unknown'

        dim_type = self.visit(node.expressions)

        print("DIM_TYPE: " + dim_type)
        if dim_type != 'multiple_expression':
            self.handle_error(self.get_error_message_for_matrix_fun(node))
            return 'unknown'
        return 'matrix'

    def visit_MatixFunctionsExpression(self, node):
        if (verbose): self.printFunctionName()

        if len(node.exprs) == 1:
            dim_type = self.visit(node.exprs[0])
            return dim_type
        elif len(node.exprs) == 2:
            dim_type1 = self.visit(node.exprs[0])
            dim_type2 = self.visit(node.exprs[1])
            if dim_type1 != dim_type2:
                return 'unknown'
            return dim_type1
        else:
            return 'unknown'

    def visit_MultipleExpression(self, node):  # designed for printing as well as matrix functions
        if (verbose): self.printFunctionName()
        for expr in node.exprs:
            if self.visit(expr) == 'unknown':
                return 'unknown'

        return 'multiple_expression'

    def visit_BooleanExpression(self, node):
        if (verbose): self.printFunctionName()
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type == 'unknown' or right_type == 'unknown':
            return 'boolean'

        return_type = self.semantic_rules.types[node.oper][left_type][right_type]
        if return_type == 'unknown':
            self.handle_error(
                'Line {}: Operation {} unsupported between types: {} and {}'.format(node.line, node.oper, left_type,
                                                                                    right_type))
        return 'boolean'

    def visit_UMinusExpression(self, node):
        if (verbose): self.printFunctionName()
        return self.visit(node.expression)

    def visit_Transposition(self, node):
        if (verbose): self.printFunctionName()
        return self.visit(node.expression)

    def visit_Rows(self, node):
        if (verbose): self.printFunctionName()
        # [ 1, 2.3;
        #  4, 5]
        # matrixOfTypes = [['int','float'], ['int', 'int']]

        matrixOfTypes = []
        for row in node.rows:
            row_types = self.visit(row)
            if row_types == 'unknown':
                return 'unknown'
            matrixOfTypes.append(row_types)

        if not len(set([len(l) for l in matrixOfTypes])) == 1:
            self.handle_error('Line {}: Matrix initialization with vectors of different sizes'.format(node.line))
            return 'unknown'
        return 'matrix'

    def visit_Row(self, node):
        if (verbose): self.printFunctionName()
        row_types = [self.visit(number) for number in node.numbers]

        if row_types.__contains__('unknown'):
            return 'unknown'
        if not len(set(row_types)) == 1:
            self.handle_error('Line {}: Matrix row initialization with different types'.format(node.line))
            return 'unknown'

        coor_type = row_types[0]
        if coor_type == 'int' or coor_type == 'float':
            return row_types

        self.handle_error('Line {}: Matrix row initialization with illegal type: {}'.format(node.line, coor_type))
        return 'unknown'

    def visit_Constant(self, node):
        if (verbose): self.printFunctionName()
        val = node.value
        if type(val) is int:
            return 'int'
        if type(val) is float:
            return 'float'

    def visit_Id(self, node):
        if (verbose): self.printFunctionName()
        try:
            symbol = self.symbol_table.get(node.name)
        except KeyError:
            self.handle_error('Line {}: Id {} is used but not declared'.format(node.line, node.name))
            return "unknown"

        return symbol.type

    def visit_Error(self, node):
        if (verbose): self.printFunctionName()
        pass

    def visit_String(self, node):
        return 'string'

    def get_error_message_for_matrix_fun(self, node):
        error_msg = 'Line {}: Illegal matrix initialization: {}({}'.format(node.line, node.func,
                                                                           node.expressions.exprs[0].name)

        if len(node.expressions.exprs) > 1:
            for i in range(1, len(node.expressions.exprs)):
                error_msg += (', {}').format(node.expressions.exprs[i].value)

        error_msg += ')'
        return error_msg
