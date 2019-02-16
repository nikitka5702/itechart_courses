def pep8_warrior(name, bases, attrs):
    newattrs = {}
    for attrname, attrvalue in attrs.items():
        if attrname.startswith('__'):
            newattrs[attrname] = attrvalue
        elif isinstance(attrvalue, types.FunctionType):
            newattrs[attrname.lower()] = attrvalue
        elif isinstance(attrvalue, type):
            newattrs[
                ''.join(n.title() for n in attrname.split('_'))
            ] = attrvalue
        else:
            newattrs[attrname.upper()] = attrvalue
    return type(name, bases, newattrs)


class Pep8Warrior(type):
    def __new__(mcls, name, bases, attrs):
        newattrs = {}
        for attrname, attrvalue in attrs.items():
            if attrname.startswith('__'):
                newattrs[attrname] = attrvalue
            elif isinstance(attrvalue, types.FunctionType):
                newattrs[attrname.lower()] = attrvalue
            elif isinstance(attrvalue, type):
                newattrs[
                    ''.join(n.title() for n in attrname.split('_'))
                ] = attrvalue
            else:
                newattrs[attrname.upper()] = attrvalue
        return super().__new__(mcls, name, bases, newattrs)
