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

class LexerError(object):
    def __init__(self, lineno, col, value):
        self.lineno = lineno
        self.col = col
        self.value = value

    def __str__(self):
        return '{self.lineno}:{self.col} Illegal character {self.value}'.format(self=self)

class ZLexer(object):
    reserved = reserved
    tokens = tokens

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

    def t_error(self, t):
        error = LexerError(t.lexer.lineno, self.col(t), t.value[0])
        print('{filename}:{error}'.format(filename=self.input_filename, 
                error=str(error)), file=sys.stderr)
        print('zc: compilation terminated with status 2', file=sys.stderr)
        exit(2)

    def __init__(self, **kwargs):
        self.lexer = lex.lex(object=self, **kwargs)

    def run(self, input_filename):
        self.input_filename = input_filename
        with open(input_filename, 'r') as input_fp:
            self.input_code = input_fp.read()
        self.lexer.input(self.input_code)

    def col(self, t):
        """
        Compute column number in input stream for a given token.
        """
        last = self.input_code.rfind('\n', 0, t.lexpos)
        if last < 0:
            last = 0
        return t.lexpos - last + 1
