import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:

    @classmethod
    def print_intended(cls, string, indent):
        print("| " * indent, string, sep='')

    @addToClass(AST.Node)
    def print_tree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def print_tree(self, indent):
        self.statements.print_tree(indent)

    @addToClass(AST.Statements)
    def print_tree(self, indent):
        for statement in self.statements:
            statement.print_tree(indent)

    @addToClass(AST.Assignment)
    def print_tree(self, indent):
        TreePrinter.print_intended(self.op, indent)
        self.lvalue.print_tree(indent + 1)
        self.expression.print_tree(indent + 1)

    @addToClass(AST.IfStatement)
    def print_tree(self, indent):
        TreePrinter.print_intended('IF', indent)
        self.condition.print_tree(indent + 1)
        TreePrinter.print_intended('THEN', indent)
        self.statement.print_tree(indent + 1)
        if self.else_statement:
            TreePrinter.print_intended('ELSE', indent)
            self.else_statement.print_tree(indent + 1)

    @addToClass(AST.WhileLoop)
    def print_tree(self, indent):
        TreePrinter.print_intended('WHILE', indent)
        self.condition.print_tree(indent + 1)
        self.statement.print_tree(indent + 1)

    @addToClass(AST.ForLoop)
    def print_tree(self, indent):
        TreePrinter.print_intended('FOR', indent)
        self.variable.print_tree(indent + 1)
        self.range.print_tree(indent + 1)
        self.statement.print_tree(indent + 1)

    @addToClass(AST.Range)
    def print_tree(self, indent):
        TreePrinter.print_intended('RANGE', indent)
        self.start.print_tree(indent + 1)
        self.end.print_tree(indent + 1)

    @addToClass(AST.BreakStatement)
    def print_tree(self, indent):
        TreePrinter.print_intended('BREAK', indent)

    @addToClass(AST.ContinueStatement)
    def print_tree(self, indent):
        TreePrinter.print_intended('CONTINUE', indent)

    @addToClass(AST.ReturnStatement)
    def print_tree(self, indent):
        TreePrinter.print_intended('RETURN')
        if self.expression:
            self.expression.print_tree(indent + 1)

    @addToClass(AST.PrintStatement)
    def print_tree(self, indent):
        TreePrinter.print_intended('PRINT', indent)
        for argument in self.arguments.matrix_values:
            argument.print_tree(indent + 1)

    @addToClass(AST.LValue)
    def print_tree(self, indent):
        if self.variable:
            self.variable.print_tree(indent)
        if self.matrix_element:
            self.matrix_element.print_tree(indent)

    @addToClass(AST.BinaryExpression)
    def print_tree(self, indent):
        TreePrinter.print_intended(self.op, indent)
        self.left.print_tree(indent + 1)
        self.right.print_tree(indent + 1)

    @addToClass(AST.UnaryExpression)
    def print_tree(self, indent):
        TreePrinter.print_intended('-', indent)
        self.expression.print_tree(indent + 1)

    @addToClass(AST.Expression)
    def print_tree(self, indent):
        # TreePrinter.print_intended('()', indent)
        self.expression.print_tree(indent)

    @addToClass(AST.IntNum)
    def print_tree(self, indent):
        TreePrinter.print_intended(self.value, indent)

    @addToClass(AST.FloatNum)
    def print_tree(self, indent):
        TreePrinter.print_intended(self.value, indent)

    @addToClass(AST.String)
    def print_tree(self, indent):
        TreePrinter.print_intended(self.value, indent)

    @addToClass(AST.Variable)
    def print_tree(self, indent):
        TreePrinter.print_intended(self.name, indent)

    @addToClass(AST.MatrixElement)
    def print_tree(self, indent):
        TreePrinter.print_intended('MATRIX ELEMENT', indent)
        self.variable.print_tree(indent + 1)
        self.i.print_tree(indent + 1)
        self.j.print_tree(indent + 1)

    @addToClass(AST.Matrix)
    def print_tree(self, indent):
        TreePrinter.print_intended('MATRIX', indent)
        for row in self.matrix.matrix_rows:
            TreePrinter.print_intended('VECTOR', indent + 1)
            for elem in row.matrix_values:
                elem.print_tree(indent + 2)

    @addToClass(AST.MatrixFunction)
    def print_tree(self, indent):
        TreePrinter.print_intended(self.function_name, indent)
        self.argument.print_tree(indent + 1)

    @addToClass(AST.Transpose)
    def print_tree(self, indent):
        TreePrinter.print_intended('TRANSPOSE', indent)
        self.expression.print_tree(indent + 1)

    @addToClass(AST.Condition)
    def print_tree(self, indent):
        TreePrinter.print_intended(self.op, indent)
        self.left.print_tree(indent + 1)
        self.right.print_tree(indent + 1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        TreePrinter.print_intended(self.error, indent)

