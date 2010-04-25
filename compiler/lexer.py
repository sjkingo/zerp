from __future__ import print_function

import ply.lex as lex

class ZLexer(object):
    reserved = {
        'begin': 'BEGIN',
        'end': 'END',
    }

    tokens = [
        'NUMBER',
        'PLUS',
        'ID', # can handle reserved keywords
    ] + list(reserved.values())

    t_PLUS = r'\+'

    t_ignore = ' \t'

    def col(self, t):
        last = self.input.rfind('\n', 0, t.lexpos)
        if last < 0:
            last = 0
        return t.lexpos - last + 1

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, debug=1, **kwargs)

    def run(self, input):
        self.input = input
        self.lexer.input(input)
        for tok in self.lexer:
            print(tok)

    def t_error(self, t):
        print('%d:%d: Illegal character \'%s\'' % (t.lexer.lineno, 
                self.col(t), t.value[0]))
        t.lexer.skip(1)

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID') # try to resolve reserved kw
        return t
