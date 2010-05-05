from __future__ import print_function

import dispatch

from symtab import SymbolTable
import ztypes

symtab = SymbolTable()

class Node(object):
    def __str__(self):
        return '<%s>' % self.type

    def __iter__(self):
        return iter(self._children)

class ProgramNode(Node):
    def __init__(self, funcs):
        self.type = 'program'
        self.funcs = funcs

    @property
    def _children(self):
        return self.funcs

class FunctionNode(Node):
    def __init__(self, id, stmt_list):
        self.type = 'function'
        self.id = id
        self.stmt_list = stmt_list

    def __str__(self):
        return '<%s \'%s\'>' % (self.type, self.id)

    @property
    def _children(self):
        return self.stmt_list

class StatementNode(Node):
    def __init__(self, exp):
        self.type = 'statement'
        self.exp = exp

    def __str__(self):
        return '<%s %s>' % (self.type, self.exp)

    @property
    def _children(self):
        return [self.exp]

class StatementListNode(Node):
    def __init__(self, stmts):
        self.type = 'statement[]'
        self.stmts = stmts

    def __str__(self):
        return '<%s %s>' % (self.type, ', '.join([str(s) for s in self.stmts]))

    def __iter__(self):
        return iter(self.stmts)

    def __len__(self):
        return len(self.stmts)

    @property
    def _children(self):
        return self.stmts

class VariableNode(Node):
    def __init__(self, type, id):
        self.type = 'variable'
        self.static_type = type
        self.id = id

        if type != 'unknown':
            # declaration, add to symbol table - unless the parser is buggy,
            # the type should be a known type
            self.real_type = ztypes.known_types[type](id)
            symtab.add(self.real_type)
        else:
            # reference, fetch from symbol table
            self.real_type = symtab.get(id)
            if self.real_type is None:
                raise Exception('variable \'%s\' undeclared' % id)
            self.static_type = self.real_type.type_name

    def __str__(self):
        return '<%s %s(\'%s\')>' % (self.type, self.static_type, self.id)

    @property
    def _children(self):
        return []

class VariableDeclNode(Node):
    def __init__(self, var_node):
        self.type = 'var_decl'
        self.var_node = var_node

    def __str__(self):
        return '<%s %s>' % (self.type, self.var_node)

    @property
    def _children(self):
        return [self.var_node]

class AssignmentNode(StatementNode):
    def __init__(self, lhs, rhs):
        self.type = 'assignment'
        self.lhs = symtab.get(lhs)
        self.rhs = rhs

        if self.lhs is None:
            raise Exception('lhs variable \'%s\' undeclared' % lhs)

    def __str__(self):
        return '<%s %s to \'%s\'>' % (self.type, self.rhs, self.lhs)

    @property
    def _children(self):
        return [self.rhs]

class ExpNode(Node):
    type = 'generic exp'

class ConstantNode(ExpNode):
    def __init__(self, val):
        self.type = 'constant'
        self.value = int(val)

    def __str__(self):
        return '<%s %d>' % (self.type, self.value)

    @property
    def _children(self):
        return []

    def generate(self):
        # use GP register %a
        print('store %d %%a' % self.value)
        print('push %a')

class BinOpNode(ExpNode):
    ops = {
        '+': 'add',
    }

    def __init__(self, left, op, right):
        self.type = 'binop'
        self.left = left
        self.op_sym = op
        self.op = self.ops[op]
        self.right = right

    def __str__(self):
        return '<%s %s \'%s\' %s>' % (self.type, self.left, self.op_sym, 
                self.right)

    @property
    def _children(self):
        return [self.left, self.right]

    def generate(self):
        print(self.op)

class FunctionCallNode(StatementNode):
    def __init__(self, name, args_exp):
        self.type = 'func_call'
        self.name = name
        self.args_exp = args_exp

    def __str__(self):
        return '<%s %s(%s)>' % (self.type, self.name, self.args_exp)

    @property
    def _children(self):
        return [self.args_exp]

    def generate(self):
        print('call %s' % self.name)

class ArgumentsNode(Node):
    def __init__(self, left, right=None):
        self.type = 'arguments'
        self.left = left
        self.right = right

    def __str__(self):
        if self.right is None:
            args = self.left
        else:
            args = '%s, %s' % (self.left, self.right)
        return '<%s %s>' % (self.type, args)

    @property
    def _children(self):
        if self.right is None:
            return [self.left]
        else:
            return [self.left, self.right]

class TreeVisitor(object):
    output = False
    codegen = False

    def __init__(self, action):
        if action == 'output':
            self.output = True
        elif action == 'codegen':
            self.codegen = True

    @dispatch.on('node')
    def visit(self, node):
        """Generic visitor; do nothing"""
        pass

    @visit.when(Node)
    def visit(self, node):
        map(self.visit, node._children)

    @visit.when(ProgramNode)
    def visit(self, node):
        if self.output:
            print(node)
        for s in node:
            self.visit(s)

    @visit.when(FunctionNode)
    def visit(self, node):
        if self.output:
            print('  %s' % node)
        self.visit(node._children)

    @visit.when(StatementNode)
    def visit(self, node):
        for s in node:
            if self.output:
                print('    %s' % s)
            self.visit(s)

    @visit.when(FunctionCallNode)
    def visit(self, node):
        for s in node:
            self.visit(s)
        if self.codegen:
            node.generate()

    @visit.when(ArgumentsNode)
    def visit(self, node):
        for s in node:
            self.visit(s)

    @visit.when(BinOpNode)
    def visit(self, node):
        map(self.visit, node._children)
        if self.codegen:
            node.generate()

    @visit.when(ConstantNode)
    def visit(self, node):
        if self.codegen:
            node.generate()
