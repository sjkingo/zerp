#!/usr/bin/env python

import argparse
import sys

from exc import *
import machine

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
            default=False, help='Be verbose in parsing and executing code')
    parser.add_argument('input_filename', help='filename of compiled code to execute (give - for stdin).')
    args = parser.parse_args()

    if args.input_filename == '-':
        fp = sys.stdin
    else:
        fp = open(args.input_filename, 'r')

    return (args, fp)

def parse_program(input_fp):
    parsed = []
    for l in input_fp.readlines():
        l = l.strip()
        if len(l) == 0 or l[0] == '#':
            continue
        split = l.split()
        parsed.append((split[0], split[1:]))
    return parsed


if __name__ == '__main__':
    args, input_fp = parse_args()
    p = parse_program(input_fp)
    m = machine.Machine(args.verbose)
    ret = m.execute(p)
    exit(ret)
