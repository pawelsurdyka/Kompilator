class Node(object):
    def __init__(self, left, right, line_no=None):
        self.left = left
        self.right = right
        self.line_no = line_no

    def accept(self, visitor):
        return visitor.visit(self)


class Program(Node):
    def __init__(self, statements, line_no=None):
        self.statements = statements
        self.line_no = line_no


class Scope(Node):
    def __init__(self, statements, line_no=None):
        self.statements = statements
        self.line_no = line_no


class Statements(Node):
    def __init__(self, statement, statements=None, line_no=None):
        self.statements = statements.statements if statements else []
        self.statements.append(statement)
        self.line_no = line_no


class Statement(Node):
    pass


class Assignment(Statement):
    def __init__(self, lvalue, op, expression, line_no=None):
        self.lvalue = lvalue
        self.op = op
        self.expression = expression
        self.line_no = line_no


class IfStatement(Statement):
    def __init__(self, condition, statement, else_statement=None, line_no=None):
        self.condition = condition
        self.statement = statement
        self.else_statement = else_statement
        self.line_no = line_no


class WhileLoop(Statement):
    def __init__(self, condition, statement, line_no=None):
        self.condition = condition
        self.statement = statement
        self.line_no = line_no


class ForLoop(Statement):
    def __init__(self, variable, range, statement, line_no=None):
        self.variable = variable
        self.range = range
        self.statement = statement
        self.line_no = line_no


class Range(Node):
    def __init__(self, start, end, line_no=None):
        self.start = start
        self.end = end
        self.line_no = line_no


class BreakStatement(Statement):
    def __init__(self, line_no=None):
        self.line_no = line_no
        pass


class ContinueStatement(Statement):
    def __init__(self, line_no=None):
        self.line_no = line_no
        pass


class ReturnStatement(Statement):
    def __init__(self, expression=None, line_no=None):
        self.expression = expression
        self.line_no = line_no


class PrintStatement(Statement):
    def __init__(self, arguments, line_no=None):
        self.arguments = arguments
        self.line_no = line_no


class LValue(Node):
    def __init__(self, variable=None, matrix_element=None, line_no=None):
        self.variable = variable
        self.matrix_element = matrix_element
        self.line_no = line_no


class Expression(Node):
    def __init__(self, expression, line_no=None):
        self.expression = expression
        self.line_no = line_no


class BinaryExpression(Expression):
    def __init__(self, op, left, right, line_no=None):
        self.op = op
        self.left = left
        self.right = right
        self.line_no = line_no


class UnaryExpression(Expression):
    def __init__(self, expression, line_no=None):
        self.expression = expression
        self.line_no = line_no


class IntNum(Expression):
    def __init__(self, value, line_no=None):
        self.value = value
        self.line_no = line_no


class FloatNum(Expression):
    def __init__(self, value, line_no=None):
        self.value = value
        self.line_no = line_no


class String(Expression):
    def __init__(self, value, line_no=None):
        self.value = value
        self.line_no = line_no


class Variable(Expression):  # ID
    def __init__(self, name, line_no=None):
        self.name = name
        self.line_no = line_no


class MatrixElement(Expression):
    def __init__(self, variable, vector, line_no=None):
        self.variable = variable
        self.vector = vector
        self.line_no = line_no


class Vector(Node):
    def __init__(self, vector_elements, line_no=None):
        self.vector_elements = vector_elements
        self.line_no = line_no


class VectorElements(Node):
    def __init__(self, vector_elements, expression, line_no=None):
        if vector_elements is not None:
            self.matrix_values = vector_elements.matrix_values + [expression]
        else:
            self.matrix_values = [expression]
        self.length = len(self.matrix_values)
        self.line_no = line_no


class MatrixFunction(Expression):
    def __init__(self, function_name, argument, line_no=None):
        self.function_name = function_name
        self.argument = argument
        self.line_no = line_no


class Transpose(Expression):
    def __init__(self, expression, line_no=None):
        self.expression = expression
        self.line_no = line_no


class Condition(Node):
    def __init__(self, op, left, right, line_no=None):
        self.op = op
        self.left = left
        self.right = right
        self.line_no = line_no


class Error(Node):
    def __init__(self, error, line_no=None):
        self.error = error
        self.line_no = line_no
