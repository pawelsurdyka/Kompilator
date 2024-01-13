import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys

sys.setrecursionlimit(10000)


class Interpreter(object):

    def __init__(self):
        self.memoryStack = MemoryStack()
        # self.declaredType = None
        # self.isFunctionScope = False

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        node.statements.accept(self)

    @when(AST.Scope)
    def visit(self, node):
        node.statements.accept(self)

    @when(AST.Statements)
    def visit(self, node):
        for statement in node.statements:
            statement.accept(self)

    @when(AST.Statement)
    def visit(self, node):
        pass

    @when(AST.Assignment)
    def visit(self, node):
        expr = node.expression.accept(self)
        if node.lvalue.variable is not None:  # zwykła zmienna
            id = node.lvalue.variable.name
            if node.op == '=':
                self.memoryStack.insert(id, expr)
                return expr
            else:  # +=, -=, *=, /=
                lvalue = self.memoryStack.get(id)
                new_expr = self.evaluate(lvalue, node.op, expr)
                self.memoryStack.set(id, new_expr)
                return new_expr
        else:  # A[0], A[0, 0]
            id = node.lvalue.matrix_element.variable.name
            indexes = node.lvalue.matrix_element.vector.accept(self)
            matrix = self.memoryStack.get(id)
            if node.op == '=':
                if len(indexes) == 1:
                    matrix[indexes[0]] = expr
                elif len(indexes) == 2:
                    matrix[indexes[0]][indexes[1]] = expr
                return expr
            else:
                if len(indexes) == 1:
                    lvalue = matrix[indexes[0]]
                    new_expr = self.evaluate(lvalue, node.op, expr)
                    matrix[indexes[0]] = new_expr
                    return new_expr
                elif len(indexes) == 2:
                    lvalue = matrix[indexes[0]][indexes[1]]
                    new_expr = self.evaluate(lvalue, node.op, expr)
                    matrix[indexes[0]][indexes[1]] = new_expr
                    return new_expr

    # TODO: self.memoryStack.push(Memory()) or sth like that
    @when(AST.IfStatement)
    def visit(self, node):
        if node.condition.accept(self):
            node.statement.accept(self)
        elif node.else_statement is not None:
            node.else_statement.accept(self)

    # TODO: self.memoryStack.push(Memory()) or sth like that
    @when(AST.WhileLoop)
    def visit(self, node):
        while node.condition.accept(self):
            try:
                node.statement.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass

    # TODO
    @when(AST.ForLoop)
    def visit(self, node):
        pass

    # TODO
    @when(AST.Range)
    def visit(self, node):
        pass

    @when(AST.BreakStatement)
    def visit(self, node):
        raise BreakException()

    @when(AST.ContinueStatement)
    def visit(self, node):
        raise ContinueException()

    @when(AST.ReturnStatement)
    def visit(self, node):
        value = node.expression.accept(self)
        raise ReturnValueException(value)

    @when(AST.PrintStatement)
    def visit(self, node):
        arguments = node.arguments.accept(self)
        for arg in arguments:
            print(arg)

    @when(AST.BinaryExpression)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return self.evaluate(r1, node.op, r2)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.Variable)
    def visit(self, node):
        return self.memoryStack.get(node.name)

    @when(AST.MatrixElement)
    def visit(self, node):
        matrix = self.memoryStack.get(node.variable.name)
        indexes = node.vector.accept(self)
        if len(indexes) == 1:
            return matrix[indexes[0]]
        elif len(indexes) == 2:
            return matrix[indexes[0]][indexes[1]]

    @when(AST.Vector)
    def visit(self, node):
        return node.vector_elements.accept(self)

    @when(AST.VectorElements)
    def visit(self, node):
        vector = [expression.accept(self) for expression in node.matrix_values]
        return vector

    @when(AST.MatrixFunction)
    def visit(self, node):
        arguments = node.argument.accept(self)
        if node.function_name == 'ZEROS':
            if len(arguments) == 1:
                return [0 for _ in range(arguments[0])]
            elif len(arguments) == 2:
                return [[0 for _ in range(arguments[1])] for _ in range(arguments[0])]
        elif node.function_name == 'ONES':
            if len(arguments) == 1:
                return [1 for _ in range(arguments[0])]
            elif len(arguments) == 2:
                return [[1 for _ in range(arguments[1])] for _ in range(arguments[0])]
        elif node.function_name == 'EYE':
            return [[1 if i == j else 0 for i in range(arguments[0])] for j in range(arguments[0])]

    @when(AST.Transpose)
    def visit(self, node):
        matrix = node.expression.accept(self)
        return list(zip(*matrix))

    @when(AST.Condition)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return self.evaluate(r1, node.op, r2)

    def evaluate(self, left, op, right):
        try:
            if op == '+' or op == '+=' or op == '.+':
                if not isinstance(left, list) and not isinstance(right, list):
                    return left + right
                elif isinstance(left, list) and isinstance(right, list):
                    if not isinstance(left[0], list) and not isinstance(right[0], list):
                        return [l + r for l, r in self.zip_(left, right)]
                    elif isinstance(left[0], list) and isinstance(right[0], list):
                        return [[a + b for a, b in self.zip_(l, r)] for l, r in self.zip_(left, right)]
            elif op == '-' or op == '-=' or op == '.-':
                if not isinstance(left, list) and not isinstance(right, list):
                    return left - right
                elif isinstance(left, list) and isinstance(right, list):
                    if not isinstance(left[0], list) and not isinstance(right[0], list):
                        return [l - r for l, r in self.zip_(left, right)]
                    elif isinstance(left[0], list) and isinstance(right[0], list):
                        return [[a - b for a, b in self.zip_(l, r)] for l, r in self.zip_(left, right)]
            elif op == '*' or op == '*=' or op == '.*':
                if not isinstance(left, list) and not isinstance(right, list):
                    return left * right
                elif isinstance(left, list) and isinstance(right, list):
                    if not isinstance(left[0], list) and not isinstance(right[0], list):
                        if op == '*' or op == '*=':
                            return sum([l * r for l, r in self.zip_(left, right)])
                        elif op == '.*':
                            return [l * r for l, r in self.zip_(left, right)]
                    elif isinstance(left[0], list) and isinstance(right[0], list):
                        if op == '*' or op == '*=':
                            return [[sum(a * b for a, b in self.zip_(row_a, col_b)) for col_b in self.zip_(*right)] for
                                    row_a in left]
                        elif op == '.*':
                            return [[a * b for a, b in self.zip_(l, r)] for l, r in self.zip_(left, right)]
            elif op == '/' or op == '/=' or op == './':
                if not isinstance(left, list) and not isinstance(right, list):
                    return left / right
                elif op == './' and isinstance(left, list) and isinstance(right, list):
                    if not isinstance(left[0], list) and not isinstance(right[0], list):
                        return [l / r for l, r in self.zip_(left, right)]
                    elif isinstance(left[0], list) and isinstance(right[0], list):
                        return [[a / b for a, b in self.zip_(l, r)] for l, r in self.zip_(left, right)]
            else:  # operatory porównania
                return eval(f'{left} {op} {right}')

        except ZeroDivisionError as e:
            print(e)
            return
        except ValueError as e:
            print(e)
            return
        print('Invalid operation')

    # zip with checking lengths
    def zip_(self, *iterables):
        lengths = set(len(seq) for seq in iterables)
        if len(lengths) != 1:
            raise ValueError("Wrong length for this operation")
        return zip(*iterables)
