LogItem = collections.namedtuple('LogItem', 'name args kwargs result')


def loghelper(func_name, f):
    def wrapped(*args, **kwargs):
        self = args[0]
        result = f(*args, **kwargs)
        self.log.append(LogItem(func_name, list(args[1:]), kwargs, result))
        return result
    return wrapped


def last_log(self):
    return self.log[::-1][:3]


class Logger(type):
    def __new__(mcls, name, bases, attrs):
        newattrs = {}
        for attrname, attrvalue in attrs.items():
            if isinstance(attrvalue, types.FunctionType) and not attrname.startswith('_'):
                newattrs[attrname] = loghelper(attrname, attrvalue)
            else:
                newattrs[attrname] = attrvalue
        newattrs['LogItem'] = LogItem
        newattrs['log'] = []
        newattrs['last_log'] = property(last_log)
        return super().__new__(mcls, name, bases, newattrs)