import AST
#import SymbolTable
from SymbolTable import VectorSymbol,VariableSymbol,MatrixSymbol,SymbolTable
from collections import defaultdict
from functools import reduce

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

ttype['+']["int"]["int"] = "int"
ttype['-']["int"]["int"] = "int"
ttype['*']["int"]["int"] = "int"
ttype['/']["int"]["int"] = "int"
ttype['<']["int"]["int"] = "logic"
ttype['>']["int"]["int"] = "logic"
ttype["<="]["int"]["int"] = "logic"
ttype[">="]["int"]["int"] = "logic"
ttype["=="]["int"]["int"] = "logic"
ttype["!="]["int"]["int"] = "logic"

ttype['+']["int"]["float"] = "float"
ttype['-']["int"]["float"] = "float"
ttype['*']["int"]["float"] = "float"
ttype['/']["int"]["float"] = "float"
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
ttype['<']["float"]["float"] = "logic"
ttype['>']["float"]["float"] = "logic"
ttype["<="]["float"]["float"] = "logic"
ttype[">="]["float"]["float"] = "logic"
ttype["=="]["float"]["float"] = "logic"
ttype["!="]["float"]["float"] = "logic"

ttype['+']['vector']['vector'] = 'vector'
ttype['-']['vector']['vector'] = 'vector'
ttype['*']['vector']['vector'] = 'vector'
ttype['/']['vector']['vector'] = 'vector'
ttype['+=']['vector']['vector'] = 'vector'
ttype['-=']['vector']['vector'] = 'vector'
ttype['*=']['vector']['vector'] = 'vector'
ttype['/=']['vector']['vector'] = 'vector'

ttype['.+']['vector']['vector'] = 'vector'
ttype['.+']['vector']['int'] = 'vector'
ttype['.+']['vector']['float'] = 'vector'
ttype['.+']['int']['vector'] = 'vector'
ttype['.+']['float']['vector'] = 'vector'

ttype['.-']['vector']['vector'] = 'vector'
ttype['.-']['vector']['int'] = 'vector'
ttype['.-']['vector']['float'] = 'vector'
ttype['.-']['int']['vector'] = 'vector'
ttype['.-']['float']['vector'] = 'vector'

ttype['.*']['vector']['vector'] = 'vector'
ttype['.*']['vector']['int'] = 'vector'
ttype['.*']['vector']['float'] = 'vector'
ttype['.*']['int']['vector'] = 'vector'
ttype['.*']['float']['vector'] = 'vector'

ttype['./']['vector']['vector'] = 'vector'
ttype['./']['vector']['int'] = 'vector'
ttype['./']['vector']['float'] = 'vector'
ttype['./']['int']['vector'] = 'vector'
ttype['./']['float']['vector'] = 'vector'

ttype['\'']['vector'][None] = 'vector'
ttype['-']['vector'][None] = 'vector'
ttype['-']['int'][None] = 'int'
ttype['-']['float'][None] = 'float'
ttype['+']['string']['string'] = 'string'


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if not hasattr(node, 'children'):
            return
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

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class TypeChecker(NodeVisitor):
    def init_visit(self):
        self.symbol_table = SymbolTable(None, 'main')
        self.errors = []
        self.loop_checker = 0

    def visit_BinExpr(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)
        op = node.bin_op

        type = ttype[op][str(type_left)][str(type_right)]
        if type is not None:
            if type == 'vector':
                if isinstance(type_left, VectorSymbol) and isinstance(type_right, VectorSymbol):
                    if type_left.size != type_right.size:
                        self.errors.append((node.line, "Vector sizes does not match in binary expression"))
                    elif type_left.type != type_right.type:
                        self.errors.append((node.line, "Types does not match in binary expression"))
            return type
        else:
            self.errors.append((node.line, "Binary expression of wrong type"))
            return None


    def visit_Variable(self, node):
        pass


