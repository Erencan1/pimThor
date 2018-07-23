"""
OneObj is to have only one instance
"""
from django.db import models, transaction
from jsonfield import JSONField
import time
"""
Question: When link list node is overwrite, the previous one remains in memory. How to remove it completely?

Test:

import gc

def callWaiter():
    for obj in gc.get_objects():
        if isinstance(obj, OneObj.WaitList):
            print(obj)

W = OneObj.WaitList

W('1')
W('2')
W('3')
callWaiter()
W.peek()
callWaiter()
"""


class OneObj(models.Model):

    onproc = False  # on processing

    class WaitList:

        firstNode = None
        lastNode = None

        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
            self.nextNode = None
            if OneObj.WaitList.lastNode:
                OneObj.WaitList.lastNode.nextNode = self
                OneObj.WaitList.lastNode = self
            else:
                OneObj.WaitList.firstNode = self
                OneObj.WaitList.lastNode = self

        @classmethod
        def peek(cls):
            args, kwargs = cls.firstNode.args, cls.firstNode.kwargs
            cls.firstNode = cls.firstNode.nextNode
            if not cls.firstNode:
                cls.lastNode = None
            return args, kwargs

    def __init__(self, *args, **kwargs):

        if OneObj.objects.count() > 1:
            raise OneObj.MultipleObjectsReturned('There is already an OneObj instance')

        super(OneObj, self).__init__(*args, **kwargs)

    jsonData = JSONField(default={'ptest_id': []})

    @classmethod
    def addPTest(cls, ptest_id):

        # add transaction request into waitlist
        OneObj.WaitList(ptest_id=ptest_id)

        if cls.onproc:
            return

        while cls.WaitList.firstNode:
            while cls.onproc:
                time.sleep(0.5)
            cls.onproc = True
            ptest_id = cls.WaitList.peek()[1]['ptest_id']
            int = cls.objects.first()
            int.jsonData['ptest_id'].append(ptest_id)
            int.save()
            cls.onproc = False

    @classmethod
    def peekPTest(cls):
        while cls.onproc:
            time.sleep(0.5)
        cls.onproc = True
        int = cls.objects.first()
        ptest_id = int.jsonData['ptest_id'].pop(0)
        int.save()
        cls.onproc = False
        return ptest_id


# class OneObj(models.Model):
#
#     def __init__(self, *args, **kwargs):
#
#         if OneObj.objects.count() > 1:
#             raise OneObj.MultipleObjectsReturned('There is already an OneObj instance')
#
#         super(OneObj, self).__init__(*args, **kwargs)
#
#     jsonData = JSONField(default={'ptest_id': []})
#
#     @classmethod
#     def addPTest(cls, ptest_id):
#         with transaction.atomic():
#             int = cls.objects.select_for_update().first()
#             int.jsonData['ptest_id'].append(ptest_id)
#             int.save()
#
#     @classmethod
#     def peekPTest(cls):
#         with transaction.atomic():
#             int = cls.objects.select_for_update().first()
#             ptest_id = int.jsonData['ptest_id'].pop(0)
#             int.save()
#         return ptest_id