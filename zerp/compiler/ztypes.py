class ZType(object):
    type_name = 'unknown'
    val = None
    id = None

    def __str__(self):
        return str('<%s(%s)>' % (self.type_name, self.id))

    def __repr__(self):
        return repr(self.val)

class Integer(ZType):
    type_name = 'integer'

    def __init__(self, id, val=None):
        self.id = id
        if val is not None:
            self.set(val)

    def __eq__(self, other):
        return self.val == other

    def set(self, val):
        self.val = int(val)

class String(ZType):
    type_name = 'string'

    def __init__(self, id, val=None):
        self.id = id
        if val is not None:
            self.set(val)

    def __eq__(self, other):
        return self.val == other

    def set(self, val):
        self.val = str(val)

known_types = {
    'integer': Integer,
    'string': String,
}
