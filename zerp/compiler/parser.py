from ply.yacc import yacc
import sys

from lexer import tokens
from tree import *

__all__ = ['run_parser']

# yacc requires these to be global... maybe (TODO)
debug = False
parser = None

def run_parser(lexer, verbose):
    global debug, parser
    debug = verbose
    parser = yacc(debug=verbose)
    return parser.parse(lexer=lexer)

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
    'VarDecl : KW_VAR IDENTIFIER COLON ZType SEMICOLON'
    v = VariableNode(p[4], p[2])
    p[0] = VariableDeclNode(v)
    print_node('VarDecl', p)

def p_ztype(p):
    '''ZType : KW_INTEGER
             | KW_STRING
    '''
    p[0] = p[1]

def p_assignment(p):
    'Assignment : IDENTIFIER ASSIGN Expression SEMICOLON'
    p[0] = AssignmentNode(p[1], p[3])
    print_node('Assignment', p)

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
                 | VarDecl
                 | Assignment'''
    p[0] = StatementNode(p[1])
    print_node('Statement', p)

def p_exp_binop(p):
    'Expression : Expression PLUS Expression'
    p[0] = BinOpNode(p[1], p[2], p[3])
    print_node('Expression', p)

def p_exp_iconst(p):
    'Expression : ICONST'
    p[0] = ConstantNode(p[1])
    print_node('Constant', p)

def p_exp_sconst(p):
    'Expression : SCONST'
    p[0] = ConstantStringNode(p[1])
    print_node('ConstantString', p)

def p_exp_var(p):
    'Expression : IDENTIFIER'
    p[0] = VariableNode('unknown', p[1])
    print_node('Variable', p)

def p_exp_func_call(p):
    'Expression : FunctionCall'
    p[0] = p[1]

def p_func_arguments(p):
    '''Arguments : Expression
                 | Expression COMMA Expression'''
    if len(p) == 2:
        p[0] = ArgumentsNode(p[1])
    else:
        p[0] = ArgumentsNode(p[1], p[3])
    print_node('Arguments', p)

def p_func_call(p):
    'FunctionCall : IDENTIFIER LPAREN Arguments RPAREN'
    p[0] = FunctionCallNode(p[1], p[3])
    print_node('FunctionCall', p)

def p_error(p):
    if p is not None:
        print('Line %d: Syntax error at token' % p.lineno, p.type, p.value)
        parser.errok()
