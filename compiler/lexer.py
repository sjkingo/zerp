from __future__ import print_function

import ply.lex as lex

reserved = {
    'begin': 'KW_BEGIN',
    'end': 'KW_END',
    'var': 'KW_VAR',
    'integer': 'KW_INTEGER',
}

tokens = [
    'NUMBER',
    'PLUS',
    'IDENTIFIER', # can handle reserved keywords
    'ASSIGN',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'COLON',
    'SEMICOLON',
] + list(reserved.values())

class ZLexer(object):
    reserved = reserved
    tokens = tokens

    errors = []

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
    t_COLON = r':'
    t_SEMICOLON = r';'

    def col(self, t):
        """Compute column number in input stream"""
        last = self.input.rfind('\n', 0, t.lexpos)
        if last < 0:
            last = 0
        return t.lexpos - last + 1

    def build(self, **kwargs):
        # why this isn't __init__ I have no idea
        self.lexer = lex.lex(module=self, **kwargs)

    def run(self, input, filename=None):
        """Take an input stream and return its tokens"""
        self.input = input
        self.filename = filename
        self.lexer.input(input)
        return (self.lexer, self.errors)

    def t_error(self, t):
        self.errors.append((t.lexer.lineno, self.col(t)))
        print('%s:%d:%d: Illegal character \'%s\'' % 
                (self.filename, t.lexer.lineno, self.col(t), t.value[0]))
        t.lexer.skip(1)

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # try and see if this token is a reserved keyword
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t
