#!/usr/bin/env python2.6

from __future__ import print_function
import sys

import lexer

def run_lexer(file):
    l = lexer.ZLexer()
    l.build()
    with open(file, 'r') as fp:
        tokens, errors = l.run(fp.read(), filename=file)
    if len(errors) != 0:
        print('%d error(s) found while lexing' % len(errors), file=sys.stderr)
    return tokens


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: %s input-file' % sys.argv[0], file=sys.stderr)
        exit(1)
    run_lexer(sys.argv[1])
