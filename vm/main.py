#!/usr/bin/env python2.6

from __future__ import print_function
from optparse import OptionParser

from exc import *
import machine

def parse_args():
    parser = OptionParser(usage='usage: %prog [options] filename')
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
            default=False, help='Be verbose in parsing and executing code')
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error('incorrect number of parameters')
    return (options, args[0])

def parse_program(filename):
    with open(filename, 'r') as fp:
        lines = fp.readlines()
    parsed = []
    for l in lines:
        l = l.strip()
        if len(l) == 0 or l[0] == '#':
            continue
        split = l.split()
        parsed.append((split[0], split[1:]))
    return parsed


if __name__ == '__main__':
    opts, filename = parse_args()
    p = parse_program(filename)
    m = machine.Machine(opts.verbose)
    ret = m.execute(p)
    exit(ret)
