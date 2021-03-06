import inspect
import logging
import pickle
import re
import string

from .exc import *

# by default debugging is switched on
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

class BuiltinFuncs(object):
    @classmethod
    def print(cls, machine, arg1):
        print(arg1)
        return 0 # always succeeds

class Stack(object):
    s = []

    def push(self, x):
        self.s.append(str(x))

    def pop(self):
        try:
            return self.s.pop()
        except IndexError:
            raise StackUnderflow()

    def print(self):
        logging.debug('+------')
        for i, f in enumerate(reversed(self.s)):
            logging.debug('| %s' % f)
        logging.debug('+------')

class Machine(object):
    stack = Stack()
    regs = {k: None for k in list(string.ascii_lowercase)}
    line = 0
    program = None

    def __init__(self, verbose):
        if not verbose:
            logging.disable(logging.DEBUG)
        self.stack.push(0) # return value

    def execute(self, program_fp):
        self.program = pickle.load(program_fp)
        try:
            for i, inst_line in enumerate(self.program['code']):
                opcode = inst_line.split()[0]
                args = inst_line.split()[1:]
                self.line = i
                try:
                    func = getattr(self, 'i_%s' % opcode)
                except AttributeError:
                    raise InvalidOpcode(opcode)
                try:
                    logging.debug('%s %s' % (opcode, ' '.join(args)))
                    func(*args)
                    logging.debug('--')
                except TypeError as e:
                    if '%s() takes' % opcode in str(e):
                        raise OpcodeArgumentsInvalid(opcode)
                    else:
                        raise # a TypeError in the function itself

            # when we're finished, the last value on the stack is used as
            # the return. (we pushed 0 at the start so provided the uesr did
            # not pop it off, we default to 0
            self.line += 1
            return int(self.stack.pop())

        except MachineException as e:
            print('%s: line %d: %s' % (e.type, self.line, e.message))
            self.halt()
            return 100

    def halt(self):
        print('Machine halted')

    def get_reg(self, reg):
        # First try to match one of the data sections before
        # checking registers

        sec_match = self._sec_patt.match(reg)
        if sec_match:
            # Program section
            section, index = sec_match.groups()
            val = self.program[section][int(index)][-1]
        else:
            # Register
            if reg[1:] not in self.regs:
                raise InvalidRegister(reg)
            val = self.regs[reg[1:]]

        logging.debug('%s -> %s' % (reg, val))
        return val

    def store_reg(self, reg, val):
        if reg[1:] not in self.regs:
            raise InvalidRegister(reg)
        self.regs[reg[1:]] = val
        logging.debug('%s <- %s' % (reg, val))

    # Machine instructions

    _sec_patt = re.compile(r'^\.([a-z]+)\[(\d+)\]')
    def i_push(self, x):
        """PUSH reg
        Push the value in the named register on to the stack."""

        val = self.get_reg(str(x))
        # Remove double quotes from start and end if present - this
        # denotes a string
        val = re.sub(r'^"|"$', '', val)
        self.stack.push(val)
        self.stack.print()

    def i_pop(self):
        """POP
        Pop the value off the stop of the stack."""

        v = self.stack.pop()
        self.stack.print()
        return v

    def i_store(self, val, reg):
        """STORE constant dest
        Store the immediate value 'constant' in the given register."""

        self.store_reg(str(reg), val)

    def i_call(self, func_name):
        """CALL name
        Call the function given by name. The arguments should be pushed on to 
        the stack in reverse order first."""

        if not hasattr(BuiltinFuncs, func_name):
            raise UnknownFunction(func_name)

        func = getattr(BuiltinFuncs, func_name)

        # get the number of arguments this function takes. We use this to
        # pop only the correct amount of arguments off the stack. Note - 2 to
        # remove the `cls` and `machine` arguments.
        n = len(inspect.getargspec(func).args) - 2

        # construct an arguments list
        args = []
        for i in range(n):
            x = self.stack.pop()
            args.append(x)

        logging.debug('Calling %s(%s)' % (func_name, ', '.join(args)))

        # call the function and capture its return. Note that this isn't a 
        # bound method so pass the machine instance.
        ret = func(self, *args)

        # Push the return back on the stack and we're done
        self.stack.push(ret)
        self.stack.print()

    def i_add(self):
        """ADD
        Adds the value on the top of the stack to the value on the second
        top of stack (popping both in the process) and pushes on the result.
        This can also be used for string concatenation."""

        v1 = self.stack.pop()
        v2 = self.stack.pop()
        self.stack.push(v1 + v2)
        self.stack.print()

    def i_sub(self):
        """SUB
        Subtract the top of the stack from the second top of stack (popping
        both values off in the process) and pushes the result on."""

        try:
            v1 = int(self.stack.pop())
            v2 = int(self.stack.pop())
        except ValueError:
            raise InvalidOpcode('Cannot perform SUB on top two stack values')
        self.stack.push(v1 - v2)
        self.stack.print()

    def i_equ(self):
        """EQU
        Compare the top of stack with the second top of stack (popping both
        off in the process) and pushes 1 if they are equal, or 0 otherwise."""

        v1 = int(self.stack.pop())
        v2 = int(self.stack.pop())
        if v1 == v2:
            self.stack.push(1)
        else:
            self.stack.push(0)
        self.stack.print()
