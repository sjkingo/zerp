#!/usr/bin/env python

import argparse

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

def main():
    args = parse_args()

    # Perform lexing
    zlex = ZLexer()
    zlex.run(args.input_filename)

    # Parse the input
    program_node = run_parser(zlex.lexer, verbose=args.verbose)
    if program_node is None:
        exit(1)

    # Generate AST and print if verbose
    tree = AST(program_node)
    if args.verbose:
        tree.dump()

    if args.stop_parser:
        exit(0)

    # Run code generation over the AST provided and output to file.
    CodeGenerator(tree).generate(args.out, verbose=args.verbose)


if __name__ == '__main__':
    main()
