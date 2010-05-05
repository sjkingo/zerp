from __future__ import print_function
import inspect

import builtins
from exc import *

class Machine(object):
    stack = []
    regs = {
        'a': 0,
        'b': 0,
    }
    line = 0
    builtins = builtins.funcs

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
                    func = getattr(self, 'i_%s' % opcode)
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
        self.debug('-- stack --')
        for f in reversed(self.stack):
            self.debug(f)
        self.debug('--')

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

    # Machine instructions

    def i_push(self, x):
        val = self.get_reg(str(x))
        self.stack.append(val)
        self.print_stack()

    def i_pop(self):
        try:
            v = self.stack.pop()
        except IndexError:
            raise StackUnderflow()
        self.print_stack()
        return v

    def i_store(self, val, reg):
        self.store_reg(str(reg), val)

    def i_call(self, func_name):
        if func_name not in self.builtins:
            raise UnknownFunction(func_name)

        func = getattr(builtins, self.builtins[func_name])

        # get the number of arguments this function takes. We use this to
        # pop only the correct amount of arguments off the stack. Note - 1 to
        # remove the machine object we will be passing.
        n = len(inspect.getargspec(func).args) - 1

        # construct an arguments list
        args = []
        for i in xrange(n):
            try:
                x = self.stack.pop()
            except IndexError:
                raise StackUnderflow()
            else:
                args.append(str(x))

        self.debug('Calling %s(%s)' % (func_name, ', '.join(args)))

        # call the function and capture its return. Note that this isn't a 
        # bound method so pass the machine instance.
        ret = func(self, *args)

        # Push the return back on the stack and we're done
        self.stack.append(str(ret))
        self.print_stack()

    def i_add(self):
        """Adds the value on the top of the stack to the value on the second
        top of stack (popping both in the process) and pushes on the result.
        """
        v1 = int(self.i_pop())
        v2 = int(self.i_pop())
        self.stack.append(v1 + v2)
        self.print_stack()
