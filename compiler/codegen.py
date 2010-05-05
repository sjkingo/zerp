from __future__ import print_function
import datetime
import os
import stat
import sys

from tree import *

class CodeGenerator(object):
    def __init__(self):
        self.visitor = TreeVisitor('codegen')

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
