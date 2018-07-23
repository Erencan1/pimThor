from django.db import models
from jsonfield import JSONField
from django.utils import timezone
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from home3.CFunction.ML import rTypes, bTypes
from django.core.files import File
import pickle
from pimThor3.settings import MEDIA_ROOT
import os
import re
from pimThor3.settings import AUTH_USER_MODEL
# from django.contrib.auth.models import Group
from .OneObj import OneObj


class Customer(models.Model):
    name = models.CharField(max_length=50)


class Zone(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    data = JSONField(default={'regrexp': {}})
    """
    data = {
        
        'regrexp': {
            
            bandType: {
            
                length_of_regrexp: [ regrexp, ...  ]
                
            }        
        }
    }
    """
    def validName(self, cn, bandType):
        try:
            for regr in self.data['regrexp'][bandType][str(len(cn))]:
                if re.compile(regr).match(cn):
                    return True
        except KeyError:
            pass
        return False

    def findBandType(self, cn):
        for btype in self.data['regrexp']:
            if self.validName(cn, btype):
                return btype
        return None


class CFunction(models.Model):
    """
    cfFile: pkl file/path
    """
    pTypes = rTypes

    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    pType = models.CharField(max_length=20, choices=pTypes)
    bType = models.CharField(max_length=20, choices=bTypes)

    name = models.CharField(max_length=30)
    run_date = models.DateTimeField(default=timezone.now)

    cfFile = models.FileField()  # (upload_to='cfFiles/%Y/%m/%d', blank=True, null=True)

    def saveFile(self, method):
        FileName = 'cfz%s%s%s' % (self.zone_id, self.pType, self.name)
        Tempo_file_path = os.path.join(MEDIA_ROOT, 'tempoFiles', FileName)
        fffp = os.path.join(MEDIA_ROOT, 'cfFiles', self.zone.name, timezone.now().strftime('%Y_%m_%d'))
        if not os.path.exists(fffp):
            os.makedirs(fffp)
        with open(Tempo_file_path, 'wb') as f:
            pickle.dump(method, f)
        with open(Tempo_file_path, 'rb') as f:
            file_wrapper = File(f)
            self.cfFile.save(os.path.join(fffp, FileName), file_wrapper, save=True)
        os.remove(Tempo_file_path)

    def getMethod(self):
        return pickle.load(open(self.cfFile.path, 'rb'))


class PTest(models.Model):
    """
    data where PRB, all other summaries of the test
    """
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    run_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=None, null=True)
    run_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    data = JSONField(default=dict)
    info = JSONField(default=dict)


class Roof(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)


class CellData(models.Model):
    """
    data where all features, parameters are
    """
    roof = models.ForeignKey(Roof, on_delete=models.CASCADE)
    ptest = models.ForeignKey(PTest, on_delete=None)
    bType = models.CharField(max_length=20, choices=bTypes)
    name = models.CharField(max_length=30)
    data = JSONField(default=dict)
    info = JSONField(default=dict)

    converted = models.BooleanField(default=False)

    def convert(self):
        """
        this is used to convert obj.data layout after analysis methods are applied
        First layout is used to analyze
        Converted layout is used to display by graphs
        This won't be proceed until a request is submit
        :return:
        """
        # this will be implemented into CreatePTest.proc
        if not self.converted:
            converted_data = {}
            times = sorted(self.data)
            converted_data['T'] = times
            for time in times:
                timedata = self.data[time]
                for header, value in timedata.items():
                    if header == 'X' and type(value) is list:
                        for i, v in enumerate(value, 0):
                            h = '%s_%s' % (header, i)
                            try:
                                converted_data[h].append(v)
                            except KeyError:
                                converted_data[h] = [v]
                    else:
                        try:
                            converted_data[header].append(value)
                        except KeyError:
                            converted_data[header] = [value]

            self.data = converted_data
            self.converted = True
            self.save()


class ExtendedUser(AbstractUser):

    _zones = models.ManyToManyField(Zone)
    _inOneInfo = JSONField(default={})

    def addZone(self, zone):
        self._zones.add(zone)

        customerName = zone.customer.name
        try:
            self._inOneInfo[customerName].append((zone.id, zone.name))
        except KeyError:
            self._inOneInfo[customerName] = [(zone.id, zone.name)]

    def removeZone(self, zone):
        self._zones.remove(zone)
        customerName = zone.customer.name
        self._inOneInfo[customerName].remove((zone.id, zone.name))
        if not len(self._inOneInfo[customerName]):
            del self._inOneInfo[customerName]

    def cust_zone_info(self):
        return self._inOneInfo

    def getZones(self, getID=True):
        if getID:
            i = 0
        else:
            i = 1
        zone_ids = []
        for ct, pt in self.cust_zone_info().items():
            for zoneIDName in pt:
                zone_ids.append(zoneIDName[i])
        return zone_ids