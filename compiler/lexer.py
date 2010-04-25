from __future__ import print_function

import ply.lex as lex

class ZLexer(object):
    reserved = {
        'begin': 'BEGIN',
        'end': 'END',
        'var': 'VAR_DECL',
        'print': 'PRINT_STMT',
    }

    tokens = [
        'NUMBER',
        'PLUS',
        'IDENTIFIER', # can handle reserved keywords
        'NEWLINE',
        'ASSIGN',
        'COMMA',
        'LPAREN',
        'RPAREN',
    ] + list(reserved.values())

    # whitespace is only meaningful to seperate tokens
    t_ignore = ' \t'

    # ignore from # to the end of a line
    t_ignore_COMMENT = r'\#.*'

    # tokens that do not require further processing
    t_PLUS = r'\+'
    t_ASSIGN = r':='
    t_COMMA = r','
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    def col(self, t):
        """Compute column number in input stream"""
        last = self.input.rfind('\n', 0, t.lexpos)
        if last < 0:
            last = 0
        return t.lexpos - last + 1

    def build(self, **kwargs):
        # why this isn't __init__ I have no idea
        self.lexer = lex.lex(module=self, debug=1, **kwargs)

    def run(self, input, filename=None):
        """Take an input stream and return its tokens"""
        self.input = input
        self.filename = filename
        self.lexer.input(input)
        return list(self.lexer)

    def t_error(self, t):
        print('%s:%d:%d: Illegal character \'%s\'' % 
                (self.filename, t.lexer.lineno, self.col(t), t.value[0]))
        t.lexer.skip(1)

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        return t # insert into token tree

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # try and see if this token is a reserved keyword
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t
