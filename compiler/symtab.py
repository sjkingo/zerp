class SymbolTable(object):
    tab = {}

    def __init__(self):
        pass

    def add(self, var):
        if var.id in self.tab:
            raise Exception('%s already in symbol table' % var.name)
        self.tab[var.id] = var

    def get(self, name):
        return self.tab.get(name, None)
