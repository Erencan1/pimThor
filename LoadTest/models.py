# NodeLoad and RoofLoad will be removed if same db is used
from django.db import models
from LoadTest.MMC import MMC
from jsonfield import JSONField
from django.utils import timezone
from django.utils.functional import SimpleLazyObject
from home3.models import ExtendedUser


class LoadUserMeta(type):

    @staticmethod
    def __call__(user):
        if type(user) == SimpleLazyObject or type(user) == ExtendedUser:
            user_id = user.id
        else:
            user_id = int(user)
        try:
            return LoadDBUserRelationMainDB.objects.get(main_user_id=user_id)
        except LoadDBUserRelationMainDB.DoesNotExist:
            if type(user) == int:
                user = ExtendedUser.objects.get(id=user_id)
            ldbu = LoadDBUserRelationMainDB()
            ldbu.main_user_id = user_id
            ldbu.username = user.username
            ldbu.save()
            return ldbu


# To establish relation between two database for user-related queries: LoadUser(userObj)
class LoadUser(metaclass=LoadUserMeta):
    pass


@MMC.setdb('load')
class LoadDBUserRelationMainDB(models.Model):
    main_user_id = models.IntegerField(blank=False, null=False)
    username = models.CharField(max_length=150)

    def __str__(self):
        return self.username


@MMC.setdb('load')
class LoadTest(models.Model):
    run_by = models.ForeignKey(LoadDBUserRelationMainDB, on_delete=None)
    run_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    data = JSONField(default=dict)
    name = models.CharField(max_length=34, default='')

    def nameIt(self):
        # random ever-changing naming may be implemented in front end
        names = list(self.data)
        if len(names) == 1:
            names = list(self.data[names[0]])   # cell based naming
        name = ','.join(names[:3])[:30]     # site based naming
        if len(names) > 3:
            name = '%s %s' % (name, '...')
        self.name = name


@MMC.setdb('load')
class NodeLoad(models.Model):
    name = models.CharField(max_length=30)


@MMC.setdb('load')
class RoofLoad(models.Model):
    node = models.ForeignKey(NodeLoad, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)


@MMC.setdb('load')
class CellLoadData(models.Model):
    test = models.ForeignKey(LoadTest, on_delete=None)
    roof = models.ForeignKey(RoofLoad, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    # data = {X_i:{T_i:V_{ij}}}
    # data = {
    #     X_M : {
    #         T_0 :   V_M0,
    #         T_1 :   V_M1,
    #         T_N:    V_MN
    #     }
    # }
    # this is different than home3.models.CellData due to irrelevant time of data
    data = JSONField(default=dict)