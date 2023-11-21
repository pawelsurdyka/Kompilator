class Node(object):
    def __str__(self):
        return self.print_tree()


class Program(Node):
    def __init__(self, statements):
        self.statements = statements


class Statements(Node):
    def __init__(self, statement, statements=None):
        self.statements = statements.statements if statements else []
        self.statements.append(statement)


class Statement(Node):
    pass


class Assignment(Statement):
    def __init__(self, lvalue, op, expression):
        self.lvalue = lvalue
        self.op = op
        self.expression = expression


class IfStatement(Statement):
    def __init__(self, condition, statement, else_statement=None):
        self.condition = condition
        self.statement = statement
        self.else_statement = else_statement


class WhileLoop(Statement):
    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement


class ForLoop(Statement):
    def __init__(self, variable, range, statement):
        self.variable = variable
        self.range = range
        self.statement = statement


class Range(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class BreakStatement(Statement):
    pass


class ContinueStatement(Statement):
    pass


class ReturnStatement(Statement):
    def __init__(self, expression=None):
        self.expression = expression


class PrintStatement(Statement):
    def __init__(self, arguments):
        self.arguments = arguments


class LValue(Node):
    def __init__(self, variable=None, matrix_element=None):
        self.variable = variable
        self.matrix_element = matrix_element


class Expression(Node):
    def __init__(self, expresssion):
        self.expression = expresssion



class BinaryExpression(Expression):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class UnaryExpression(Expression):
    def __init__(self, expression):
        self.expression = expression



class IntNum(Expression):
    def __init__(self, value):
        self.value = value


class FloatNum(Expression):

    def __init__(self, value):
        self.value = value


class String(Expression):

    def __init__(self, value):
        self.value = value


class Variable(Expression):  # ID
    def __init__(self, name):
        self.name = name


class MatrixElement(Expression):
    def __init__(self, variable, i, j):
        self.variable = variable
        self.i = i
        self.j = j


class Matrix(Expression):
    def __init__(self, matrix):
        self.matrix = matrix


class MatrixRows(Node):
    def __init__(self, matrix_rows, matrix_values):
        if matrix_rows is not None:
            self.matrix_rows = matrix_rows.matrix_rows + [matrix_values]
        else:
            self.matrix_rows = [matrix_values]


class MatrixValues(Node):
    def __init__(self, matrix_values, expression):
        if matrix_values is not None:
            self.matrix_values = matrix_values.matrix_values + [expression]
        else:
            self.matrix_values = [expression]


class MatrixFunction(Expression):
    def __init__(self, function_name, argument):
        self.function_name = function_name
        self.argument = argument


class Transpose(Expression):
    def __init__(self, expression):
        self.expression = expression


class Condition(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Error(Node):
    def __init__(self, error):
        self.error = error
