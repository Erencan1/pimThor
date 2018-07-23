"""
    @author:            Erencan Yilmaz

    The MMC wrapper is used to make Django ORM for only the specified database
        ~ No need DB Router
        ~ No need .using(database_name)
    @MMC.setdb('DB2')
    class Person(models.Model):
        name = models.CharField(max_length=30)
    p = Person.objects.first()
    p.name, p.save()... -> won't hit the default database but they will hit DB2!
    This is valid for all Django ORM operations.
    This also allows the database to switch in the live system.
        MMC.setdb('DB3')(Person)
"""


class MMC:
    @classmethod
    def setdb(cls, db, methods=None):
        if methods is None or type(methods) is not list:
            methods = [
                'save',
                'delete',
                'refresh_from_db',
                'save_base',
            ]

        def set_db(the_class):

            the_class._mmc_db_name = db
            for method in methods:
                cls._add_using(the_class, method)

            the_class.objects = the_class.objects.using(db)
            return the_class

        return set_db

    @staticmethod
    def _add_using(the_class, method):
        fun = getattr(the_class, method)

        def mfun(*args, **kwargs):
            kwargs['using'] = the_class._mmc_db_name
            return fun(*args, **kwargs)

        setattr(the_class, method, mfun)