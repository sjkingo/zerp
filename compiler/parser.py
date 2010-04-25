from __future__ import print_function

import ply.yacc as yacc

from ast import *
from lexer import tokens

debug = False

def uniqify(l):
    n = []
    [n.append(i) for i in l if not n.count(i) and i is not None]
    return n

def print_node(name, children):
    if not debug:
        return
    print('%s: %s' % (name, list(children)))
    for c in list(children):
        print('  %s' % str(c))

# never put anything above here!
def p_program(p):
    'Program : Function' 
    p[0] = ProgramNode([p[1]])
    print_node('Program', p)

def p_empty(p):
    'e : '
    pass

def p_function(p):
    'Function : KW_BEGIN IDENTIFIER LPAREN RPAREN StatementList KW_END'
    p[0] = FunctionNode(p[2], p[5])
    print_node('Function', p)

def p_var_decl(p):
    'VarDecl : KW_VAR IDENTIFIER COLON IDENTIFIER SEMICOLON'
    p[0] = VariableNode(p[4], p[2])
    print_node('VarDecl', p)

def p_statement_list(p):
    '''StatementList : StatementList Statement
                     | e'''

    # merge any children into us and add one single StatementList
    l = uniqify(p)
    sl = []
    for i in l:
        if type(i) is StatementListNode:
            if len(i) != 0:
                sl.extend(i)
        else:
            sl.append(i)

    if len(sl) != 0:
        p[0] = StatementListNode(sl)
    print_node('StatementList', p)

def p_statement_exp(p):
    '''Statement : Expression SEMICOLON
                 | VarDecl'''
    p[0] = StatementNode(p[1])
    print_node('Statement', p)

def p_exp_binop(p):
    'Expression : Expression PLUS Expression'
    p[0] = BinOpNode(p[1], p[2], p[3])
    print_node('Expression', p)

def p_exp_constant(p):
    'Expression : NUMBER'
    p[0] = ConstantNode(p[1])
    print_node('Constant', p)

def p_error(p):
    if p is not None:
        print('Syntax error at token %s' % p.type)
        yacc.errok()

class ZParser(object):
    def run(self, lexer):
        self.parser = yacc.yacc(debug=True, outputdir='out')
        return self.parser.parse(lexer=lexer)
