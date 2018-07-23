from home3.CFunction.ML import mLs
from home3 import models


class CCFs:

    def __init__(self, niceX, niceY, zone, ptype, btype, sourceInfo=None):
        """
        :param niceX:   filtered X
        :param niceY:   filtered Y
        :param zone:    zone obj
        :param ptype:   PUSCH or PUSSH
        :param btype:   band type
        """
        self.zone = zone
        self.ptype = ptype
        self.btype = btype
        self.sourceInfo = sourceInfo

        for ml in mLs:
            self._saveToDB(ml(niceX, niceY))

    def _saveToDB(self, method):

        methodName = '%s_%s_%s_%s' % (method.name, self.zone.name, self.ptype, self.btype)

        method.zone = self.zone.name
        method.ptype = self.ptype
        method.btype = self.btype
        method.sourceInfo = self.sourceInfo

        # TO DB

        cf = models.CFunction()
        cf.zone = self.zone
        cf.pType = self.ptype
        cf.bType = self.btype
        cf.name = methodName
        cf.saveFile(method)
