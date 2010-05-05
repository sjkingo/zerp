from __future__ import print_function

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
        print('call print')

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
        print('store %d %%a' % node.value)
        print('push %a')
