# import AST
# #import SymbolTable
# from SymbolTable import VectorSymbol,VariableSymbol,MatrixSymbol,SymbolTable
# from collections import defaultdict
# from functools import reduce

from collections import defaultdict

import AST
import SymbolTable

symtab = SymbolTable.SymbolTable(None, "Symtab")
typo = False

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

ttype['+']["int"]["int"] = "int"
ttype['-']["int"]["int"] = "int"
ttype['*']["int"]["int"] = "int"
ttype['/']["int"]["int"] = "int"
ttype[".+"]["int"]["int"] = "int"
ttype[".-"]["int"]["int"] = "int"
ttype[".*"]["int"]["int"] = "int"
ttype["./"]["int"]["int"] = "int"
ttype['<']["int"]["int"] = "logic"
ttype['>']["int"]["int"] = "logic"
ttype["<="]["int"]["int"] = "logic"
ttype[">="]["int"]["int"] = "logic"
ttype["=="]["int"]["int"] = "logic"
ttype["!="]["int"]["int"] = "logic"
ttype[':']["int"]["int"] = "int"

ttype['+']["int"]["float"] = "float"
ttype['-']["int"]["float"] = "float"
ttype['*']["int"]["float"] = "float"
ttype['/']["int"]["float"] = "float"
ttype[".+"]["int"]["float"] = "float"
ttype[".-"]["int"]["float"] = "float"
ttype[".*"]["int"]["float"] = "float"
ttype["./"]["int"]["float"] = "float"
ttype['<']["int"]["float"] = "logic"
ttype['>']["int"]["float"] = "logic"
ttype["<="]["int"]["float"] = "logic"
ttype[">="]["int"]["float"] = "logic"
ttype["=="]["int"]["float"] = "logic"
ttype["!="]["int"]["float"] = "logic"

ttype['+']["float"]["int"] = "float"
ttype['-']["float"]["int"] = "float"
ttype['*']["float"]["int"] = "float"
ttype['/']["float"]["int"] = "float"
ttype[".+"]["float"]["int"] = "float"
ttype[".-"]["float"]["int"] = "float"
ttype[".*"]["float"]["int"] = "float"
ttype["./"]["float"]["int"] = "float"
ttype['<']["float"]["int"] = "logic"
ttype['>']["float"]["int"] = "logic"
ttype["<="]["float"]["int"] = "logic"
ttype[">="]["float"]["int"] = "logic"
ttype["=="]["float"]["int"] = "logic"
ttype["!="]["float"]["int"] = "logic"

ttype['+']["float"]["float"] = "float"
ttype['-']["float"]["float"] = "float"
ttype['*']["float"]["float"] = "float"
ttype['/']["float"]["float"] = "float"
ttype[".+"]["float"]["float"] = "float"
ttype[".-"]["float"]["float"] = "float"
ttype[".*"]["float"]["float"] = "float"
ttype["./"]["float"]["float"] = "float"
ttype['<']["float"]["float"] = "logic"
ttype['>']["float"]["float"] = "logic"
ttype["<="]["float"]["float"] = "logic"
ttype[">="]["float"]["float"] = "logic"
ttype["=="]["float"]["float"] = "logic"
ttype["!="]["float"]["float"] = "logic"

ttype['*']["str"]["int"] = "str"

castable_operations = ['/', '+', '-', '*', '>', '<', ">=", "<=", "==", "!="]
castable_matrix_operations = [".+", ".-", ".*", "./"]
castable_types = ["int", "float"]


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):
    def visit_Node(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Program(self, node):
        symtab.pushScope("scope")
        self.visit(node.statements)
        symtab.popScope()

    def visit_Scope(self, node):
        symtab.pushScope("scope")
        self.visit(node.statements)
        symtab.popScope()

    def visit_Statements(self, node):
        self.visit(node.statements)

    def visit_ContinueStatement(self, node):
        loop_scope = symtab.getScope("loop")
        if not loop_scope:
            # ERROR
            print("Continue outside loop scope", node.line_no)
            pass

    def visit_BreakStatement(self, node):
        loop_scope = symtab.getScope("loop")
        if not loop_scope:
            # ERROR
            print('Break outside loop scope', node.line_no)
            pass

    def visit_Assignment(self, node):
        a = self.visit(node.expression)
        if node.op != '=':
            if symtab.get(node.lvalue.variable.name) is None:
                print("Undeclared variable", node.line_no)
                return
        if node.lvalue.variable is None:
            if symtab.get(node.lvalue.matrix_element.variable.name) is None:
                print("Undeclared variable", node.line_no)
        else:
            symtab.put(node.lvalue.variable.name, a)
        # if isinstance(node.expression, AST.MatrixFunction):
        #     symtab.put(node.lvalue.variable.name, node.expression.function_name)

    def visit_Variable(self, node):
        var = symtab.get(node.name)
        if var:
            return symtab.get(node.name).type
        print("Undeclared variable", node.line_no)
        return None

    def visit_IntNum(self, node):
        return "int"

    def visit_FloatNum(self, node):
        return "float"

    def visit_String(self, node):
        return "str"

    def visit_ReturnStatement(self, node):
        function_scope = symtab.getScope("function")
        if not function_scope:
            # ERROR
            print('Return outside function scope', node.line_no)
            pass
        if node.expression:
            self.visit(node.expression)

    def visit_Vector(self, node):
        # wektor wektorów tj.macierz
        if isinstance(node.vector_elements.matrix_values[0], AST.Vector):
            n = node.vector_elements.matrix_values[0].vector_elements.length
            for column in node.vector_elements.matrix_values:
                if isinstance(column, AST.Vector):
                    n_i = column.vector_elements.length
                    if n != n_i:
                        print("Matrix with rows of different lengths ", node.line_no)
                        break
                else:
                    print("Matrix can be initialized only with vectors! ", node.line_no)
                    break
            return "Matrix", (node.vector_elements.length, n)
        else:
            self.visit(node.vector_elements)
            return "Vector", node.vector_elements.length

    def visit_VectorElements(self, node):
        self.visit(node.matrix_values)

    def visit_ForLoop(self, node):
        symtab.pushScope("loop")
        var = node.variable
        # if variable in for range is not declared
        if not symtab.get(var.name):
            symtab.put(var.name, "int")
            self.visit(node.variable)
        self.visit(node.statement)
        self.visit(node.range)
        symtab.popScope()

    def visit_WhileLoop(self, node):
        symtab.pushScope("loop")
        self.visit(node.statement)
        symtab.popScope()

    def visit_IfStatement(self, node):
        self.visit(node.statement)

    def visit_Expression(self, node):
        return self.visit(node.expression)

    # TODO: błędy w przypadku MatrixElement
    def visit_BinaryExpression(self, node):
        l_type = self.visit(node.left)
        r_type = self.visit(node.right)
        if not isinstance(l_type, tuple):  # int, float, str
            if isinstance(r_type, tuple):  # vector matrix
                print("Different types (uncastable)", l_type, r_type[0], node.line_no)
                return
            else:
                if r_type not in ttype[node.op][l_type]:
                    print("Different types (uncastable)", l_type, r_type, node.line_no)
                    return
                else:
                    return ttype[node.op][l_type][r_type]
        elif l_type[0] == 'Vector':
            if not isinstance(l_type, tuple):
                print("Different types (uncastable)", l_type[0], r_type, node.line_no)
                return
            elif r_type[0] == 'Matrix':
                print("Different types (uncastable)", l_type[0], r_type[0], node.line_no)
                return
            else:  # vector and vector
                #     if len(node.left.matrix_values) != len(node.right.matrix_values):
                #         print("Vectors with different lengths", node.line_no)
                #         return
                if node.op == '*':
                    return "float"  # lub int?
                elif node.op == '/':
                    print("Wrong operation for vectors", node.op, node.line_no)
                    return
                else:
                    return l_type  # pytanie czy nie trzeba jakiejś kopii zrobić

        elif l_type[0] == 'Matrix':
            if not isinstance(l_type, tuple):
                print("Different types (uncastable)", l_type[0], r_type, node.line_no)
                return
            elif r_type[0] == 'Vector':
                print("Different types (uncastable)", l_type[0], r_type[0], node.line_no)
                return
            else:  # matrix and matrix
                return l_type  # trzeba dołożoć sprawdzenie wymiarów

    def visit_Range(self, node):
        s_type = self.visit(node.start)
        e_type = self.visit(node.end)
        if s_type != "int" or e_type != "int":
            print("Range have to be form int to int ", node.line_no)
        if s_type == None or e_type == None:
            print("Undeclared variables in range scope ", node.line_no)

    def visit_PrintStatement(self, node):
        self.visit(node.arguments)

    def visit_UnaryExpression(self, node):
        return self.visit(node.expression)

    def visit_Transpose(self, node):
        type1 = self.visit(node.expression)
        if not isinstance(type1, tuple):
            # error
            print("Trying to transpose non-matrix entity", node.line_no)
            pass

    def visit_LValue(self, node):
        if node.variable is not None:
            self.visit(node.variable)
        elif node.matrix_element is not None:
            self.visit(node.matrix_element)

    def visit_MatrixElement(self, node):
        self.visit(node.variable)
        self.visit(node.vector)

    def visit_MatrixFunction(self, node):
        name = node.function_name
        n_arguments = node.argument.length
        if name == 'EYE' and n_arguments != 1:
            print("Wrong number of arguments in function", name, node.line_no)
            return
        elif n_arguments != 1 and n_arguments != 2:
            print("Wrong number of arguments in function", name, node.line_no)
            return
        else:
            self.visit(node.argument)

        if isinstance(node.argument.matrix_values[0], AST.Variable):
            first_arg = symtab.get(
                node.argument.matrix_values[0].name)  # jeśli jest zmienna to będzie tylko typ a nie wartość
        else:
            first_arg = node.argument.matrix_values[0].value

        if name == 'EYE':
            return "Matrix", (first_arg, first_arg)
        elif n_arguments == 2:
            if isinstance(node.argument.matrix_values[0], AST.Variable):
                second_arg = symtab.get(node.argument.matrix_values[1].name)
            else:
                second_arg = node.argument.matrix_values[1].value
            return "Matrix", (first_arg, second_arg)
        else:
            return "Vector", first_arg

    def visit_Condition(self, node):
        l_side = self.visit(node.left)
        r_side = self.visit(node.rigth)
        if l_side != r_side:
            print("Wrong elements in condition", node.line_no)
