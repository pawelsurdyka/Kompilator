from scanner import Scanner

import AST
from colorama import Fore, Style


class Mparser(object):
    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()
        self.is_error = False

    tokens = Scanner.tokens

    precedence = (
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ('right', 'ASSIGN', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
        ('left', 'LT', 'GT', 'LE', 'GE', 'NE', 'EQ'),
        ('left', 'PLUS', 'MINUS', 'DOTADD', 'DOTSUB'),
        ('left', 'TIMES', 'DIVIDE', 'DOTMUL', 'DOTDIV'),
        ('right', 'UMINUS'),
        ('right', 'TRANSPOSE'),
    )

    def p_error(self, p):
        self.is_error = True
        print(Fore.RED, end='')
        if p:
            print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
        else:
            print("Unexpected end of input")
        print(Style.RESET_ALL, end='')

    def p_program(self, p):
        """
        program : statements
        """
        p[0] = AST.Program(p[1], line_no=self.scanner.lexer.lineno)

    def p_statements(self, p):
        """
        statements : statement
        """
        p[0] = AST.Statements(p[1], line_no=self.scanner.lexer.lineno)

    def p_statements2(self, p):
        """
        statements : statements statement
        """
        p[0] = AST.Statements(p[2], p[1], line_no=self.scanner.lexer.lineno)

    def p_statement(self, p):
        """
        statement : if_statement
                   | while_loop
                   | for_loop
                   | return_statement
                   | print_statement
                   | assignment
        """
        p[0] = p[1]

    def p_statement2(self, p):
        """
        statement : break_statement
        """
        p[0] = AST.BreakStatement(line_no=self.scanner.lexer.lineno)

    def p_statement3(self, p):
        """
        statement : continue_statement
        """
        p[0] = AST.ContinueStatement(line_no=self.scanner.lexer.lineno)

    def p_statement_brace(self, p):
        """
        statement : LBRACE statements RBRACE
        """
        p[0] = p[2]

    def p_assignment(self, p):
        """
        assignment : lvalue ASSIGN expression SEMICOLON
                    | lvalue ADDASSIGN expression SEMICOLON
                    | lvalue SUBASSIGN expression SEMICOLON
                    | lvalue MULASSIGN expression SEMICOLON
                    | lvalue DIVASSIGN expression SEMICOLON
        """
        p[0] = AST.Assignment(p[1], p[2], p[3], line_no=self.scanner.lexer.lineno)

    def p_matrix_element(self, p):
        """
        matrix_element : ID LBRACKET vector_elements RBRACKET
        """
        p[0] = AST.MatrixElement(AST.Variable(p[1]), p[3], line_no=self.scanner.lexer.lineno)

    def p_lvalue_matrix_element(self, p):
        """
        lvalue : matrix_element
        """
        p[0] = AST.LValue(matrix_element=p[1], line_no=self.scanner.lexer.lineno)

    def p_lvalue_id(self, p):
        """
        lvalue : ID
        """
        p[0] = AST.LValue(variable=AST.Variable(p[1]), line_no=self.scanner.lexer.lineno)

    def p_expression(self, p):
        """
        expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression
        """
        p[0] = AST.BinaryExpression(p[2], p[1], p[3], line_no=self.scanner.lexer.lineno)

    def p_expression_in_par(self, p):
        """
        expression : LPAREN expression RPAREN
        """
        p[0] = AST.Expression(p[2], line_no=self.scanner.lexer.lineno)

    def p_expression_floatnum(self, p):
        """
        expression : FLOATNUM
        """
        p[0] = AST.FloatNum(p[1], line_no=self.scanner.lexer.lineno)

    def p_expression_intnum(self, p):
        """
        expression : INTNUM
        """
        p[0] = AST.IntNum(p[1], line_no=self.scanner.lexer.lineno)

    def p_expression_string(self, p):
        """
        expression : STRING
        """
        p[0] = AST.String(p[1], line_no=self.scanner.lexer.lineno)

    def p_expression_id(self, p):
        """
        expression : ID
        """
        p[0] = AST.Variable(p[1], line_no=self.scanner.lexer.lineno)

    def p_expression_matrix_element(self, p):
        """
        expression : matrix_element
        """
        p[0] = p[1]

    def p_expression_unary(self, p):
        """
        expression : MINUS expression %prec UMINUS
        """
        p[0] = AST.UnaryExpression(p[2], line_no=self.scanner.lexer.lineno)

    def p_expression_transpose(self, p):
        """
        expression : expression TRANSPOSE
        """
        p[0] = AST.Transpose(p[1], line_no=self.scanner.lexer.lineno)

    def p_condition(self, p):
        """
        condition : expression LT expression
                 | expression GT expression
                 | expression LE expression
                 | expression GE expression
                 | expression NE expression
                 | expression EQ expression
        """
        p[0] = AST.Condition(p[2], p[1], p[3], line_no=self.scanner.lexer.lineno)

    def p_matrix_expression(self, p):
        """
        expression : matrix_function
                    | vector
        """
        p[0] = p[1]

    def p_statement_eye(self, p):
        """
        matrix_function : EYE LPAREN vector_elements RPAREN
        """
        p[0] = AST.MatrixFunction('EYE', p[3], line_no=self.scanner.lexer.lineno)

    def p_statement_zeros(self, p):
        """
        matrix_function : ZEROS LPAREN vector_elements RPAREN
        """
        p[0] = AST.MatrixFunction('ZEROS', p[3], line_no=self.scanner.lexer.lineno)

    def p_statement_ones(self, p):
        """
        matrix_function : ONES LPAREN vector_elements RPAREN
        """
        p[0] = AST.MatrixFunction('ONES', p[3], line_no=self.scanner.lexer.lineno)

    def p_if_statement(self, p):
        """
        if_statement : IF LPAREN condition RPAREN statement %prec IFX
        """
        p[0] = AST.IfStatement(p[3], p[5], line_no=self.scanner.lexer.lineno)

    def p_if_else_statement(self, p):
        """
        if_statement : IF LPAREN condition RPAREN statement ELSE statement
        """
        p[0] = AST.IfStatement(p[3], p[5], p[7], line_no=self.scanner.lexer.lineno)

    def p_while_loop(self, p):
        """
        while_loop : WHILE LPAREN condition RPAREN statement
        """
        p[0] = AST.WhileLoop(p[3], p[5], line_no=self.scanner.lexer.lineno)

    def p_for_loop(self, p):
        """
        for_loop : FOR ID ASSIGN range statement
        """
        p[0] = AST.ForLoop(AST.Variable(p[2]), p[4], p[5], line_no=self.scanner.lexer.lineno)

    def p_range(self, p):
        """
        range : expression COLON expression
        """
        p[0] = AST.Range(p[1], p[3], line_no=self.scanner.lexer.lineno)

    def p_break_statement(self, p):
        """
        break_statement : BREAK SEMICOLON
        """
        p[0] = AST.BreakStatement(line_no=self.scanner.lexer.lineno)

    def p_continue_statement(self, p):
        """
        continue_statement : CONTINUE SEMICOLON
        """
        p[0] = AST.ContinueStatement(line_no=self.scanner.lexer.lineno)

    def p_return_statement(self, p):
        """
        return_statement : RETURN SEMICOLON
        """
        p[0] = AST.ReturnStatement(line_no=self.scanner.lexer.lineno)

    def p_return_statement2(self, p):
        """
        return_statement : RETURN expression SEMICOLON
        """
        p[0] = AST.ReturnStatement(p[2], line_no=self.scanner.lexer.lineno)

    def p_print_statement(self, p):
        """
        print_statement : PRINT vector_elements SEMICOLON
        """
        p[0] = AST.PrintStatement(p[2], line_no=self.scanner.lexer.lineno)

    def p_vector(self, p):
        """
        vector : LBRACKET vector_elements RBRACKET
        """
        p[0] = AST.Vector(p[2], line_no=self.scanner.lexer.lineno)

    def p_vector_elements(self, p):
        """
        vector_elements : expression
        """
        p[0] = AST.VectorElements(None, p[1], line_no=self.scanner.lexer.lineno)

    def p_vector_elements2(self, p):
        """
        vector_elements : vector_elements COMMA expression
        """
        p[0] = AST.VectorElements(p[1], p[3], line_no=self.scanner.lexer.lineno)
