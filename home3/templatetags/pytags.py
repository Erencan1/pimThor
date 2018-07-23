from django import template
register = template.Library()


@register.filter(name='is_dict')
def is_dict(st):
    if type(st) is dict:
        return True
    return False


@register.filter(name='dict_path')
def dict_path(the_dict, path=[]):
    for k, v in the_dict.items():
        if type(v) is dict:
            for yld in dict_path(v, path+[k]):
                yield yld
        else:
            yield ('-'.join(path+[k]), v)