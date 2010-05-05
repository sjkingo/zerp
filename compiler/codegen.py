from __future__ import print_function
import datetime
import os
import stat
import sys

import dispatch

from tree import *

class CodeGenVisitor(object):
    @dispatch.on('node')
    def visit(self, node):
        """Generic visitor; do nothing"""
        pass

    @visit.when(Node)
    def visit(self, node):
        """Start at the top-level tree node"""
        map(self.visit, node._children)

    @visit.when(FunctionNode)
    def visit(self, node):
        self.visit(node._children)

    @visit.when(StatementNode)
    def visit(self, node):
        for s in node:
            self.visit(s)

    @visit.when(FunctionCallNode)
    def visit(self, node):
        for s in node:
            self.visit(s)
        print('call %s' % node.name)

    @visit.when(ArgumentsNode)
    def visit(self, node):
        for s in node:
            self.visit(s)

    @visit.when(BinOpNode)
    def visit(self, node):
        map(self.visit, node._children)
        print(node.op)

    @visit.when(ConstantNode)
    def visit(self, node):
        """We store the immediate value in a register and push it on to the
        stack."""
        print('store %d %%a' % node.value)
        print('push %a')

class CodeGenerator(object):
    def __init__(self):
        self.visitor = CodeGenVisitor()

    def generate(self, filename, tree):
        fp = open(filename, 'w')

        # override stdout to go to the file
        sys._stdout = sys.stdout
        sys.stdout = fp

        # write header
        vm_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 
                '..', 'vm', 'main.py'))
        print('#!%s' % vm_path)
        print('# compiled at %s' % datetime.datetime.now())

        # generate the code
        self.visitor.visit(tree)

        # restore stdout
        sys.stdout = sys._stdout
        del sys._stdout
        fp.close()

        # add execute permissions; +x
        os.chmod(filename, 0755)
