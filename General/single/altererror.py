def altererror(alter_function, *alter_args, **alter_kwargs):

    def fun(function):

        def context(*args, **kwargs):

            try:
                return function(*args, **kwargs)
            except:
                if len(alter_args) or len(alter_args):
                    return alter_function(*alter_args, **alter_kwargs)
                else:
                    return alter_function(*args, **kwargs)

        return context

    return fun


def hidError(fun):
    def y(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except Exception as e:
            error = e
        raise ValueError(error)
    return y


class Argument:
    def __init__(self, main_args, main_kwargs, exception, alter_args, alter_kwargs):
        self.main_args = main_args
        self.main_kwargs = main_kwargs
        self.exception = exception
        self.alter_args = alter_args
        self.alter_kwargs = alter_kwargs


def alter_arg_error(alter_function, *alter_args, **alter_kwargs):

    def fun(function):
        def context(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                return alter_function(Argument(
                    args, kwargs, e, alter_args, alter_kwargs
                ))
        return context

    return fun