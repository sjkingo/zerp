from __future__ import print_function

funcs = {
    'print': 'print_func',
}

def print_func(machine, arg1):
    print(arg1)
    return 0 # always succeeds
