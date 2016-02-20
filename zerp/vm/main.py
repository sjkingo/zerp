#!/usr/bin/env python

import argparse
import sys

from .exc import *
from .machine import Machine

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
            default=False, help='Be verbose in parsing and executing code')
    parser.add_argument('input_filename', help='filename of compiled code to execute (give - for stdin).')
    args = parser.parse_args()

    if args.input_filename == '-':
        fp = sys.stdin
    else:
        fp = open(args.input_filename, 'rb')

    return (args, fp)

def main():
    args, input_fp = parse_args()
    m = Machine(args.verbose)
    ret = m.execute(input_fp)
    exit(ret)


if __name__ == '__main__':
    main()
