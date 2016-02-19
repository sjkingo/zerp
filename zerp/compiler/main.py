#!/usr/bin/env python

from optparse import OptionParser, OptionGroup
import sys

import codegen
import lexer
import parser
import tree

def parse_args():
    parser = OptionParser(usage='usage: %prog [options] input-filename',
            description='The zerp compiler compiles a source file written in '
            'the Z programming language into an executable program that can '
            'run on the zerp stack machine.')

    # basic options
    parser.add_option('-o', dest='out', metavar='FILE', default='z.out',
            help='write executable output to FILE (defaults to %default)')
    parser.add_option('-v', dest='verbose', action='store_true',
            default=False, help='be verbose during all stages of compiling')

    # stop after x phase
    stop_group = OptionGroup(parser, 'Stop after phase', 'These options can '
            'be used to stop the compiler after it finishes a particular '
            'phase.')
    stop_group.add_option('-p', dest='stop_parser', action='store_true',
            default=False, help='stop after parsing and output an abstract '
            'syntax tree (this implies -v)')
    parser.add_option_group(stop_group)

    # parse the arguments
    opts, args = parser.parse_args()
    if len(args) != 1:
        parser.error('incorrect number of parameters')

    # fix up implied options
    if opts.stop_parser:
        opts.verbose = True

    return (opts, args[0])

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

    l = run_lexer(filename, verbose=opts.verbose)
    p = run_parser(l, verbose=opts.verbose)
    if opts.verbose:
        v = tree.TreeVisitor('output')
        print('-- AST --')
        v.visit(p) # print out the AST
        print('--')
    if opts.stop_parser:
        exit(0)

    run_generator(opts.out, p)
