import sys
import ply.lex as lex


class Scanner(object):

    def build(self):
        self.lexer = lex.lex(object=self)

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()

    tokens = (
        'ID',
        'INTNUM',
        'FLOATNUM',
        'STRING',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'LPAREN',
        'RPAREN',
        'LBRACKET',
        'RBRACKET',
        'LBRACE',
        'RBRACE',
        # 'NUMBER',
        'DOTADD',
        'DOTSUB',
        'DOTMUL',
        'DOTDIV',
        'ASSIGN',
        'ADDASSIGN',
        'SUBASSIGN',
        'MULASSIGN',
        'DIVASSIGN',
        'LT',
        'GT',
        'LE',
        'GE',
        'NE',
        'EQ',
        'COLON',
        'TRANSPOSE',
        'COMMA',
        'SEMICOLON',
        'IF',
        'ELSE',
        'FOR',
        'WHILE',
        'BREAK',
        'CONTINUE',
        'RETURN',
        'EYE',
        'ZEROS',
        'ONES',
        'PRINT',
    )

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_DOTADD = r'\.\+'
    t_DOTSUB = r'\.-'
    t_DOTMUL = r'\.\*'
    t_DOTDIV = r'\./'
    t_ASSIGN = r'='
    t_ADDASSIGN = r'\+='
    t_SUBASSIGN = r'-='
    t_MULASSIGN = r'\*='
    t_DIVASSIGN = r'/='
    t_LT = r'<'
    t_GT = r'>'
    t_LE = r'<='
    t_GE = r'>='
    t_NE = r'!='
    t_EQ = r'=='
    t_COLON = r':'
    t_TRANSPOSE = r'\''
    t_COMMA = r','
    t_SEMICOLON = r';'

    t_ignore = ' \t'

    # Słowa kluczowe
    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'for': 'FOR',
        'while': 'WHILE',
        'break': 'BREAK',
        'continue': 'CONTINUE',
        'return': 'RETURN',
        'eye': 'EYE',
        'zeros': 'ZEROS',
        'ones': 'ONES',
        'print': 'PRINT',
    }

    def t_newline(self, t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)

    def t_comment(self, t):
        r"""\#.*"""
        pass

    def t_ID(self, t):
        r"""[a-zA-Z_][a-zA-Z_0-9]*"""
        t.type = Scanner.reserved.get(t.value, 'ID')
        return t

    def t_FLOATNUM(self, t):
        r"""(\d+\.\d*|\.\d+)([Ee][+-]?\d+)?"""
        t.value = float(t.value)
        return t

    def t_INTNUM(self, t):
        r"""\d+([Ee][+-]?\d+)?"""
        if 'E' in t.value or 'e' in t.value:
            t.type = 'FLOATNUM'
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'\"([^\\\n]|(\\.))*?\"'
        return t

    def t_error(self, t):
        print("line %d: illegal character '%s'" % (t.lexer.lineno, t.value[0]))
        t.lexer.skip(1)