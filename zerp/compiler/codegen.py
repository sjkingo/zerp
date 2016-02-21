from collections import OrderedDict
from multipledispatch import dispatch
from pprint import pprint
import os
import pickle

from .tree import *
from .ztypes import *

__all__ = ['CodeGenerator']

_SECTION_NAMES = ['strings', 'code']

class CodeGenerator(object):
    sections = OrderedDict((k, []) for k in _SECTION_NAMES)

    def __init__(self, tree):
        self.tree = tree

    # Dispatch methods go here. This is used to generate actions for each type
    # of node in the AST.

    @dispatch(FunctionNode)
    def store_node(self, node):
        pass

    @dispatch(StatementNode)
    def store_node(self, node):
        pass

    @dispatch(AssignmentNode)
    def store_node(self, node):
        pass

    @dispatch(ConstantNode)
    def store_node(self, node):
        pass

    @dispatch(VariableNode)
    def store_node(self, node):
        if type(node.ztype) == String:
            self._string(node)

    @dispatch(ReferenceNode)
    def store_node(self, node):
        if type(node.vardecl_node.ztype) == String:
            name = node.vardecl_node.identifier
            index = self._get_string_tuple(name)[0]
            node.location = index
        self._code(node)

    @dispatch(ArgumentsNode)
    def store_node(self, node):
        self._code(node)

    @dispatch(FunctionCallNode)
    def store_node(self, node):
        self._code(node)

    @dispatch(BinOpNode)
    def store_node(self, node):
        self._code(node)

    # Internal helper functions to tidy up the dispatch methods

    def _string(self, node):
        """
        Store the string specified in node.
        """
        index = len(self.sections['strings'])
        self.sections['strings'].append((index, node.identifier, node.value.value))

    def _code(self, node):
        """
        Generate code for the given node and store it.
        """
        c = node.generate()
        if c is None:
            return
        if type(c) == str:
            c = [c]
        self.sections['code'].extend(c)

    def _get_string_tuple(self, identifier):
        for index, name, value in self.sections['strings']:
            if identifier == name:
                return (index, name, value)
        return None

    # External methods

    def dump(self):
        """
        Dump human-readable program to stdout.
        """

        print('\n-- Start of program dump --\n')
        for section_name, items in self.sections.items():
            print('.section', section_name)
            for i in items:
                print('  ', i)
        print('\n-- End of program dump --')

    def generate(self, output_filename, verbose):
        """
        Run the code generator over the AST and place the resulting output in
        the file specified.
        """

        # Walk down the whole AST and generate code
        self.tree.visit(callback=self.store_node)

        if verbose:
            self.dump()

        # Write pickled binary code to the file specified
        with open(output_filename, 'wb') as fp:
            pickle.dump(self.sections, fp, protocol=-1)
