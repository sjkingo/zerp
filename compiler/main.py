#!/usr/bin/env python2.6

from __future__ import print_function
from optparse import OptionParser

import codegen
import lexer
import parser
from tree import walk_tree

def parse_args():
    parser = OptionParser(usage='usage: %prog [options] filename')
    parser.add_option('-o', dest='out', metavar='FILE', default='z.out',
            help='Write executable output to FILE (defaults to z.out)')

    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
            default=False, help='Be verbose during all stages of compiling')
    parser.add_option('-l', dest='lexer_verbose', action='store_true',
            default=False, help='Be verbose during lexing')
    parser.add_option('-p', dest='parser_verbose', action='store_true',
            default=False, help='Be verbose during parsing')
    parser.add_option('-a', dest='ast_verbose', action='store_true',
            default=False, help='Be verbose whilst generating the AST')
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error('incorrect number of parameters')
    return (options, args[0])

def run_lexer(file, verbose):
    """Runs the lexer over contents of file and returns the instance for
    parsing."""
    l = lexer.ZLexer()
    l.build(debug=verbose)
    with open(file, 'r') as fp:
        lex, errors = l.run(fp.read(), filename=file)
    if len(errors) != 0:
        print('%d error(s) found while lexing' % len(errors), file=sys.stderr)
    return lex

def run_parser(lex, verbose):
    p = parser.ZParser()
    return p.run(lex, verbose)

def run_generator(dest_filename, tree):
    c = codegen.CodeGenerator()
    c.generate(dest_filename, tree)


if __name__ == '__main__':
    opts, filename = parse_args()
    lexer_verbose = opts.verbose or opts.lexer_verbose
    parser_verbose = opts.verbose or opts.parser_verbose
    ast_verbose = opts.verbose or opts.ast_verbose

    l = run_lexer(filename, verbose=lexer_verbose)
    p = run_parser(l, verbose=parser_verbose)
    if ast_verbose:
        walk_tree(p)

    run_generator(opts.out, p)
