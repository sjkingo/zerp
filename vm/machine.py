from __future__ import print_function

from exc import *

class Machine(object):
    stack = []
    regs = {
        'a': 0,
        'b': 0,
    }
    line = 0

    def __init__(self, verbose):
        self.verbose = verbose
        self.stack.append(0) # return value

    def debug(self, msg):
        if self.verbose:
            print('DEBUG: %s' % msg)

    def execute(self, ins):
        try:
            for i, (opcode, args) in enumerate(ins):
                self.line = i
                try:
                    func = getattr(self, opcode)
                except AttributeError:
                    raise InvalidOpcode(opcode)
                try:
                    self.debug('%s %s' % (opcode, ' '.join(args)))
                    func(*args)
                    self.debug('--')
                except TypeError, e:
                    if '%s() takes' % opcode in str(e):
                        raise OpcodeArgumentsInvalid(opcode)
                    else:
                        raise # a TypeError in the function itself

            # when we're finished, the last value on the stack is used as
            # the return. (we pushed 0 at the start so provided the uesr did
            # not pop it off, we default to 0
            self.line += 1
            try:
                return int(self.stack.pop())
            except IndexError:
                raise StackUnderflow()

        except MachineException, e:
            print('%s: line %d: %s' % (e.type, self.line, e.message))
            self.halt()
            return 100

    def print_stack(self):
        print('-- stack --')
        for f in reversed(self.stack):
            print(f)
        print('--')

    def halt(self):
        print('Machine halted')

    def get_reg(self, reg):
        if reg[1:] not in self.regs:
            raise InvalidRegister(reg)
        val = self.regs[reg[1:]]
        self.debug('%s -> %s' % (reg, val))
        return val

    def store_reg(self, reg, val):
        if reg[1:] not in self.regs:
            raise InvalidRegister(reg)
        self.regs[reg[1:]] = val
        self.debug('%s <- %s' % (reg, val))

    def push(self, x):
        val = self.get_reg(str(x))
        self.stack.append(val)
        self.print_stack()

    def pop(self):
        try:
            self.stack.pop()
        except IndexError:
            raise StackUnderflow()
        self.print_stack()

    def store(self, val, reg):
        self.store_reg(str(reg), val)
