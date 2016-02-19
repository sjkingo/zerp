import ply.lex as lex
import sys

# Reserved keywords
reserved = {
    'begin': 'KW_BEGIN',
    'end': 'KW_END',
    'var': 'KW_VAR',
    'integer': 'KW_INTEGER',
    'string': 'KW_STRING',
}

# All valid tokens
tokens = list(reserved.values()) + [
    # Literals (integer constant, string constant)
    'IDENTIFIER', 'ICONST', 'SCONST',

    # Delimeters , ( ) : ;
    'COMMA', 'LPAREN', 'RPAREN', 'COLON', 'SEMICOLON',

    # Operators +
    'PLUS',

    # Assignment =
    'ASSIGN',
]

class ZLexer(object):
    reserved = reserved
    tokens = tokens

    errors = []

    # whitespace is only meaningful to seperate tokens
    t_ignore = ' \t'

    # ignore from # to the end of a line
    t_ignore_COMMENT = r'\#.*'

    # Literals

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # try and see if this token is a reserved keyword
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t

    def t_ICONST(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    t_SCONST = r'\"([^\\\n]|(\\.))*?\"'

    # Delimeters
    t_COMMA = r','
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_COLON = r':'
    t_SEMICOLON = r';'

    # Operators
    t_PLUS = r'\+'

    # Assignment
    t_ASSIGN = r':='

    # Handle newline and keep track of line number
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Some basic error handling of invalid characters
    def t_error(self, t):
        self.errors.append((t.lexer.lineno, self.col(t)))
        print('%s:%d:%d: Illegal character \'%s\'' % 
                (self.filename, t.lexer.lineno, self.col(t), t.value[0]), file=sys.stderr)
        t.lexer.skip(1)

    # Helper methods from here

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def run(self, input, filename=None):
        self.input = input
        self.filename = filename
        self.lexer.input(input)
        return (self.lexer, self.errors)

    def col(self, t):
        """
        Compute column number in input stream for a given token.
        """
        last = self.input.rfind('\n', 0, t.lexpos)
        if last < 0:
            last = 0
        return t.lexpos - last + 1
