class Node(object):
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
    def __init__(self, stmt_list):
        self.type = 'function'
        self.stmt_list = stmt_list

    def __str__(self):
        return str(self.stmt_list)

    @property
    def _children(self):
        return self.stmt_list

class StatementNode(Node):
    def __init__(self, exp):
        self.type = 'statement'
        self.exp = exp

    def __str__(self):
        return str(self.exp)

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

class BinOpNode(ExpNode):
    def __init__(self, left, op, right):
        self.type = 'binop'
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return '<%s %s %s %s>' % (self.type, self.left, self.op, self.right)

    @property
    def _children(self):
        return [self.left, self.right]

def walk_tree(program_root):
    if type(program_root) is not ProgramNode:
        print('walk_tree() was not passed a ProgramNode')
        return

    print(program_root.type)
    for funcs in program_root:
        print('  %s' % funcs.type)
        print('    %s' % funcs._children.type)
        for stmt in funcs:
            print('      %s' % stmt)
