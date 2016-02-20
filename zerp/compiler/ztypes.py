class ZType(object):
    type_name = 'unknown'

    def __init__(self, identifier, value=None):
        self.identifier = identifier
        self.value = value

    def __str__(self):
        return str('<%s(%s)>' % (self.type_name, self.identifier))

    def __repr__(self):
        return repr(self.value)

    def __eq__(self, other):
        return self.value == other

class Integer(ZType):
    type_name = 'integer'

class String(ZType):
    type_name = 'string'

known_types = {
    'integer': Integer,
    'string': String,
}
