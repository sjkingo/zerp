#!/usr/bin/env python

import argparse
import sys

from .codegen import CodeGenerator
from .lexer import ZLexer
from .parser import run_parser
from .tree import AST

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

def run_lexer(filename, verbose):
    """
    Runs the lexer over contents of filename and returns the instance for
    parsing.
    """

    l = ZLexer()
    l.build(debug=verbose)

    with open(filename, 'r') as fp:
        lex, errors = l.run(fp.read(), filename=filename)
        if len(errors) != 0:
            print('%d error(s) found while lexing' % len(errors), file=sys.stderr)

    return lex

def main():
    args = parse_args()

    lex = run_lexer(args.input_filename, verbose=args.verbose)

    program_node = run_parser(lex, verbose=args.verbose)
    if program_node is None:
        exit(1)

    tree = AST(program_node)
    if args.verbose:
        tree.dump()

    if args.stop_parser:
        exit(0)

    # Run code generation over the AST provided and output to file.
    CodeGenerator(tree).generate(args.out, verbose=args.verbose)


if __name__ == '__main__':
    main()
