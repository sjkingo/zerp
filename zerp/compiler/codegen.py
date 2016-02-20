from contextlib import redirect_stdout
import datetime
import os

import sys
sys.path.insert(0, os.path.realpath(os.path.join('..', '..')))
from zerp import __version__

from tree import *

class CodeGenerator(object):
    def __init__(self):
        self.visitor = TreeVisitor(codegen=True)

    def generate(self, filename, tree):
        with open(filename, 'w') as fp:
            with redirect_stdout(fp):
                # write header and generate the code
                vm_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 
                        '..', 'vm', 'main.py'))
                print('#!%s' % vm_path)
                print('# compiled at %s by zerp %s' % (datetime.datetime.now(), __version__))
                print('# using compiler arguments: %s' % ' '.join(sys.argv))
                self.visitor.visit(tree)

        # add execute permissions; +x
        os.chmod(filename, 0o755)
