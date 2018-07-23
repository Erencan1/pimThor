# Not completely tested
from General.single.altererror import hidError


class TheDict(dict):

    @staticmethod
    def _type(v):
        return type(v) in [dict, TheDict]

    @hidError
    def find(*args):
        the_dict, keyWord = args
        for k, v in the_dict.items():
            if k == keyWord:
                yield v
            if TheDict._type(v):
                for y in TheDict.find(v, keyWord):
                    yield y

    @hidError
    def key_path(*args, subpath=[]):
        the_dict = args[0]
        for k, v in the_dict.items():
            if TheDict._type(v):
                for y in TheDict.key_path(v, subpath=subpath + [k]):
                    yield y
            else:
                yield subpath + [k], v
                # yield '%s   =   %s' % (str(subpath + [k]).strip('[]').replace(',', '->'), str(v))

    @hidError
    def copy(*args):
        the_dict, keyWord, copyWord = args
        add_copy = []
        for k, v in the_dict.items():
            if k == keyWord:
                add_copy.append(v)
            elif TheDict._type(v):
                TheDict.copy(v, keyWord, copyWord)
        for v in add_copy:
            the_dict[copyWord] = v

    @hidError
    def insert(*args, force=False):
        the_dict, *args = args
        args = list(args)
        v = args.pop()
        last_arg = args.pop()
        for arg in args:
            if (TheDict._type(the_dict) and arg not in the_dict) or (force and not TheDict._type(the_dict[arg])):
                the_dict[arg] = {}
            the_dict = the_dict[arg]
        if not force and (not TheDict._type(the_dict) or last_arg in the_dict):
            if TheDict._type(the_dict):
                p, va = next(TheDict.key_path(the_dict, last_arg))
                msg = '%s   :   %s' % (str(p).strip('[]').replace(',', '->'), str(va))
            else:
                msg = 'non-dict %s (%s)\nUse object.key_path() to display all values' % (the_dict, type(the_dict))
            raise ValueError('Already occupied \n%s\nSet force=True to update' % msg)
        the_dict[last_arg] = v
        return v
