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

        # self.shouldThrowUndeclaredIdError = False
        # self.visit(node.id)
        # self.shouldThrowUndeclaredIdError = True
        if right_type == 'matrix':
            matrix = node.expression
            if isinstance(matrix, AST.MatrixFunctions):
                dim1 = 1
                dim2 = matrix.expressions.exprs[0].value
            elif isinstance(matrix, AST.Expression):  # it's a matrix expression
                dim1 = self.symbol_table.get(matrix.left.value).dim1  # might be done differently as well
                dim2 = self.symbol_table.get(matrix.left.value).dim2
            else:  # it's a Rows object
                dim1, dim2 = self.get_matrix_dimensions(matrix)
            symbol = VariableSymbol(name=node.id.value, type=right_type, dim1=dim1, dim2=dim2)
        else:
            symbol = Symbol(name=node.id.value, type=right_type)
        self.symbol_table.put(node.id.value, symbol)
        return right_type

    def visit_AssignOperators(self, node):  # x += , -=, *=, /=
        if (verbose): self.printFunctionName()

        right_type = self.visit(node.expression)
        # a += [1,2,3] + [1,2,3];

        if right_type == 'unknown':
            return 'unknown'
        try:
            symbol = self.symbol_table.get(node.id.value)
        except KeyError:
            print('Line {}: Id {} used but undeclared'.format(node.line, node.id.value))
            return 'unknown'
        left_type = symbol.type

        return_type = self.semantic_rules.types[node.oper][left_type][right_type]

        if return_type == 'unknown':
            self.handle_error('Line {}: Unsupported operation between {} {}'.format(node.line, left_type, right_type))
            return 'unknown'

        if left_type == 'matrix' and right_type == 'matrix':
            if isinstance(node.expression, AST.Id):
                right_matrix = self.symbol_table.get(node.expression.value)
                right_dim1 = right_matrix.dim1
                right_dim2 = right_matrix.dim2
            elif isinstance(node.expression, AST.Rows):
                right_matrix = node.expression
                right_dim1, right_dim2 = self.get_matrix_dimensions(right_matrix)
            else:
                print("-------------------")
                return 'unknown'  # it should be impossible
            left_dim_1 = symbol.dim1
            left_dim_2 = symbol.dim2

            if left_dim_1 != right_dim1 or left_dim_2 != right_dim2:
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

    def visit_Ref(self, node):  # x[1,2] FIXME: x = [1,2,3]; x[1,2] = 3;
        if (verbose): self.printFunctionName()
        node_name = self.visit(node.id)
        symbol = self.symbol_table.get(node_name)
        ind1_type = self.visit(node.ind1)
        ind2_type = self.visit(node.ind2)

        for t in {ind1_type, ind2_type}:
            if t != 'unknown' and t != 'int':  # TODO: sprawdzić, czy jest niesiony
                self.handle_error('Line {}: index is not integer'.format(node.line))
                return 'unknown'

        if not symbol:
            self.handle_error('Line {}: {} is used but not declared'.format(node.line, node.variable.name))
            return 'unknown'
        if symbol.type == 'unknown':
            return 'unknown'
        elif symbol.type != 'matrix':
            self.handle_error('Line {}: Reference to: {}'.format(node.line, symbol.type))
            return 'unknown'

    def visit_Expression(self, node):
        if (verbose): self.printFunctionName()
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type == 'unknown' or right_type == 'unknown':
            return 'unknown'

        if left_type == 'matrix' and right_type == 'matrix':
            left_dim1 = self.symbol_table.get(node.left.value).dim1
            left_dim2 = self.symbol_table.get(node.left.value).dim2  # FIXME
            right_dim1 = self.symbol_table.get(node.right.value).dim1
            right_dim2 = self.symbol_table.get(node.right.value).dim2

            if node.oper=='*' and left_dim2 == right_dim1:
                return 'matrix'
            if left_dim1 != right_dim1 or left_dim2 != right_dim2:
                self.handle_error('Line {}: Unsupported operation between matrices of different dimensions'.format(node.line))
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
        dim_type = self.visit(node.expressions)

        if dim_type != 'int':
            self.handle_error(self.get_error_message_for_matrix_fun(node))
            return 'unknown'

        return 'matrix'

    def visit_MultipleExpression(self, node):
        if (verbose): self.printFunctionName()

        if len(node.exprs) > 1:
            return 'unknown'

        expr_type = self.visit(node.exprs[0])

        return expr_type

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

        if row_types.__contains__('unknown'):  # FIXME x = [a,2,3] should throw Id is unknown exc.
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
        return 'string'

    def visit_Id(self, node):
        if (verbose): self.printFunctionName()
        try:
            symbol = self.symbol_table.get(node.value)
        except KeyError:
            if self.shouldThrowUndeclaredIdError:
                self.handle_error('Line {}: Id {} is used but not declared'.format(node.line, node.value))
            return "unknown"

        return symbol.type

    def visit_Error(self, node):
        if (verbose): self.printFunctionName()
        pass

    def get_error_message_for_matrix_fun(self, node):
        error_msg = 'Line {}: Illegal matrix initialization: {}({}'.format(node.line, node.func,node.expressions.exprs[0].value)

        if len(node.expressions.exprs) > 1:
            for i in range(1, len(node.expressions.exprs)):
                error_msg += (', {}').format(node.expressions.exprs[i].value)

        error_msg += ')'
        return error_msg
