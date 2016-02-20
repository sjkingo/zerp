from multipledispatch import dispatch
import string
import sys

from .symtab import SymbolTable
from .ztypes import known_types

symtab = SymbolTable()

_regs = {k: None for k in list(string.ascii_lowercase)}
def put_reg(node, val):
    """
    Puts the given value in the next available reg and returns the key.
    """
    free_reg = [k for k, v in _regs.items() if v is None][0]
    _regs[free_reg] = (node, val)
    return free_reg

class Node(object):
    node_type = 'unknown_node'

    def __str__(self):
        return '<%s>' % self.node_type

    def __iter__(self):
        return iter([])

    def generate(self):
        return None

class ProgramNode(Node):
    node_type = 'program'

    def __init__(self, funcs):
        self.funcs = funcs

    def __iter__(self):
        return iter(self.funcs)

class FunctionNode(Node):
    node_type = 'function'

    def __init__(self, id, stmt_list):
        self.id = id
        self.stmt_list = stmt_list

    def __str__(self):
        return '<%s \'%s\'>' % (self.node_type, self.id)

    def __iter__(self):
        return iter(self.stmt_list)

class StatementNode(Node):
    node_type = 'statement'

    def __init__(self, exp):
        self.exp = exp

    def __str__(self):
        return '<%s %s>' % (self.node_type, self.exp)

    def __iter__(self):
        return iter([self.exp])

class StatementListNode(Node):
    node_type = 'statement[]'

    def __init__(self, stmts):
        self.stmts = stmts

    def __str__(self):
        return '<%s %s>' % (self.node_type, ', '.join([str(s) for s in self.stmts]))

    def __iter__(self):
        return iter(self.stmts)

    def __len__(self):
        return len(self.stmts)

class VariableNode(Node):
    """
    This node represents a variable - its declaration, type and value.
    """

    node_type = 'variable'
    
    value = None

    def __init__(self, ztype_str, identifier):
        self.identifier = identifier
        self.ztype = known_types[ztype_str](identifier)
        symtab.add(self)

    def __str__(self):
        return '<%s %s "%s" %s>' % (self.node_type, self.ztype.type_name, self.identifier, self.value)

class ReferenceNode(Node):
    """
    This node represents a reference to a VariableNode.
    """

    node_type = 'reference'

    def __init__(self, identifier):
        self.identifier = identifier
        self.vardecl_node = symtab.get(self.identifier)
        if self.vardecl_node is None:
            raise Exception('reference `%s` undeclared' % self.identifier)

    def __str__(self):
        return '<%s %s %s>' % (self.node_type, self.identifier, self.vardecl_node)

class AssignmentNode(Node):
    node_type = 'assignment'

    def __init__(self, variable, exp):
        self.variable = symtab.get(variable)
        if self.variable is None:
            raise Exception('lhs variable \'%s\' undeclared' % variable)
        self.exp = exp
        symtab.add_value(variable, exp)

    def __str__(self):
        return '<%s %s to \'%s\'>' % (self.node_type, self.exp, self.variable)

    def __iter__(self):
        return iter([self.exp])

    @property
    def value(self):
        return self.exp

class ConstantNode(Node):
    def __init__(self, val):
        self.node_type = type(val).__name__
        self.value = val
        self.reg = put_reg(self, self.value)

    def __str__(self):
        return '<%s %s>' % (self.node_type, self.value)

    def generate(self):
        return 'store %s %%%s' % (self.value, self.reg)

class BinOpNode(Node):
    node_type = 'binop'
    ops = {
        '+': 'add',
    }

    def __init__(self, left, op, right):
        self.left = left
        self.op_sym = op
        self.op = self.ops[op]
        self.right = right

    def __str__(self):
        return '<%s %s \'%s\' %s>' % (self.node_type, self.left, self.op_sym, 
                self.right)

    def __iter__(self):
        return iter([self.left, self.right])

    def generate(self):
        return self.op

class FunctionCallNode(Node):
    node_type = 'func_call'

    def __init__(self, name, args_node):
        self.name = name
        self.args_node = args_node

    def __str__(self):
        return '<%s %s(%s)>' % (self.node_type, self.name, self.args_node)

    def generate(self):
        # First generate the stack push calls for the arguments
        self.args_node.generate()
        return 'call %s' % self.name

class ArgumentsNode(Node):
    node_type = 'arguments'

    def __init__(self, subexp):
        self.subexp = subexp

    def __str__(self):
        return '<%s %s>' % (self.node_type, str(self.subexp))

class AST(object):
    """
    This is the AST for the Z program after it is parsed by the compiler.
    """

    def __init__(self, program_node):
        self.root = program_node

    def visit(self, node=None, callback=None):
        """
        Visit the node given and recursively go top-down to its descendants.
        """

        if node is None:
            node = self.root

        for c in node:
            if callback:
                callback(c)
            self.visit(c, callback=callback)

    def dump(self):
        print('\n\n-- Start of AST --')
        self.visit(callback=print)
        print('-- End of AST --')
