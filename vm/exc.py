class MachineException(Exception):
    type = 'Unknown machine exception'
    message = '??'

class StackUnderflow(MachineException):
    type = 'Stack underflow'
    message = 'Tried to pop stack when it was empty'

class OpcodeArgumentsInvalid(MachineException):
    type = 'Invalid arguments'
    def __init__(self, opcode):
        self.message = 'Invalid arguments for opcode %s' % opcode

class InvalidOpcode(MachineException):
    type = 'Invalid opcode'
    def __init__(self, opcode):
        self.message = 'Invalid opcode %s' % opcode

class InvalidRegister(MachineException):
    type = 'Invalid register'
    def __init__(self, reg):
        self.message = 'Invalid register %s' % reg

class UnknownFunction(MachineException):
    type = 'Unknown function'
    def __init__(self, func):
        self.message = 'Unknown function %s' % func
