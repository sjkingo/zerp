from __future__ import print_function

from machine import Machine

def get_ins_docs():
    """Extract the docstring from each instruction method and return a dict
    of type {op: ([args], desc}. It expects the docstrings to be in the format:

        OP [arg1, arg2, ...]
        This is a freelance description of the operation.
    """

    ops = {}
    for o in Machine.__dict__.keys():
        if not o.startswith('i_'):
            continue
        lines = getattr(Machine, o).__doc__.split('\n')
        first_line = lines[0].split()
        doc = [l.strip() for l in lines[1:]]
        ops[first_line[0]] = (first_line[1:], doc)
    return ops

def write_ins_docs(ops, filename='instructions.txt'):
    with open(filename, 'w') as fp:
        for k, (args, desc) in ops.items():
            fp.write('%s %s\n' % (k, ' '.join(args)))
            for l in desc:
                fp.write('  %s\n' % (l))
            fp.write('\n')


if __name__ == '__main__':
    ops = get_ins_docs()
    write_ins_docs(ops)
