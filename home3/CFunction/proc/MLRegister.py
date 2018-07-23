# MLRegister.element is a decorator
class MLRegister:
    mLs = []
    mLs_list = []

    @classmethod
    def element(cls, the_class):
        if not all(_ in the_class.__dict__ for _ in ['name', '__init__', '__call__']):
            raise AttributeError('%s has to have name attribute & __init__ and __call__ methods' % the_class)
        cls.mLs.append(the_class)
        cls.mLs_list.append(the_class.name)