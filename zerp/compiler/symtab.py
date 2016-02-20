class SymbolTable(object):
    """
    Symbol table for the compiler. This behaves mostly like a set, except has
    some extra methods to help the parser and code generator phases remember
    variables. You should not attempt to access the `_table` directly.
    """

    _table = {}

    def __str__(self):
        from pprint import pformat
        return pformat(self._table)

    def add(self, var_node):
        """
        Adds the given variable node to the symbol table.
        """
        if var_node is None:
            raise Exception('variable node is None?')
        if var_node.identifier in self._table:
            raise Exception('%s already in symbol table' % var_node.name)
        self._table[var_node.identifier] = var_node

    def get(self, name):
        """
        Returns the variable node for the given identifier, or None if it is
        not present in the symbol table.
        """
        return self._table.get(name, None)

    def add_value(self, name, value):
        """
        Attaches a value to the variable node stored in the symbol table.
        """
        if name not in self._table:
            raise Exception('%s not in symbol table' % name)
        self._table[name].value = value
