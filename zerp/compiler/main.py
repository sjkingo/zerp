#!/usr/bin/env python

import argparse
import sys

import codegen
import lexer
from parser import run_parser
import tree

def parse_args():
    parser = argparse.ArgumentParser(
            description='The zerp compiler compiles a source file written in '
            'the Z programming language into an executable program that can '
            'run on the zerp stack machine.')

    # basic options
    parser.add_argument('-o', dest='out', metavar='FILE', default='z.out',
            help='write executable output to FILE (defaults to %(default)s)')
    parser.add_argument('-v', dest='verbose', action='store_true',
            default=False, help='be verbose during all stages of compiling')
    parser.add_argument('input_filename', help='filename of Z program to compile')

    # stop after x phase
    stop_group = parser.add_argument_group('Stop after phase', 'These options can '
            'be used to stop the compiler after it finishes a particular '
            'phase.')
    stop_group.add_argument('-p', dest='stop_parser', action='store_true',
            default=False, help='stop after parsing and output an abstract '
            'syntax tree (this implies -v)')

    args = parser.parse_args()
    if args.stop_parser:
        args.verbose = True

    return args

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

def run_generator(dest_filename, tree):
    c = codegen.CodeGenerator()
    c.generate(dest_filename, tree)


if __name__ == '__main__':
    args = parse_args()

    l = run_lexer(args.input_filename, verbose=args.verbose)
    p = run_parser(l, verbose=args.verbose)
    if p is None:
        exit(1)

    if args.verbose:
        v = tree.TreeVisitor(output=True)
        print('\n\n-- Start of AST --')
        v.visit(p) # print out the AST
        print('-- End of AST --')
    if args.stop_parser:
        exit(0)

    run_generator(args.out, p)
