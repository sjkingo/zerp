from ply.yacc import yacc

class Exp(object):
    pass

class Constant(Exp):
    def __init__(self, val):
        self.type = 'constant'
        self.value = int(val)

def p_expression_constant(p):
    'expression : NUMBER'
    p[0] = Constant(p[1])

class ZParser(object):
    def __init__(self):
        self.parser = yacc.yacc(outputdir='out')

    def run(self, lexer):
        self.parser.parse(lexer=lexer)
