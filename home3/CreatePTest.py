from .shred import shredCell
from .CategorizeColumn import CategorizeColumns
from home3.Analysis.PRBMethod import PRBAvgMethod, PRBCellMethod
from home3.Analysis.LiMethod import LiCellMethod
from home3.Analysis.IdealTrend import IdealCellTrend
from home3.models import PTest, CFunction, Zone
from home3.Analysis.MIXTURE import MIXTURE
from home3.Analysis.Leap import Leap
from home3.CFunction.ML import bTypes
from threading import Thread
from General import randomSet, sendMail


class VerifyZone:

    def __init__(self, zone, someCellNames):

        self.someCellNames = someCellNames
        self.zone = self.clarifyZonebyCellName(zone)

    def verifyZoneByCellName(self, zone):
        for cellName in self.someCellNames:
            bandType = zone.findBandType(cellName)
            if not bandType:
                return False
        return True

    def clarifyZonebyCellName(self, zone):

        if self.verifyZoneByCellName(zone):
            # belongs to this zone
            return zone

        for otherZone in Zone.objects.all():
            if self.verifyZoneByCellName(otherZone):
                # belongs to other Zone
                return otherZone
        # belongs to none, OK to test
        return zone


def verifyDateFormat(time_sample):
    # has not been implemented
    # tempo
    try:
        date = time_sample.split()
        y, m, d = date[0].split('-')
        h, m = date[1].split(':')
        if len(y) != 4 or len(m) != 2 or len(h) != 2 or len(m) != 2 or len(d) != 2:
            raise
    except:
        print(time_sample)
        raise NameError('Date Format is wrong. Format is year/month/day hour:minute (2018-05-06 03:02)')


def CreateTestData(user, zone, filepaths, testName, prb):

    data = CategorizeColumns(filepaths, prb=prb).FileData
    data = {k: v.values for k, v in data.items()}
    for _ in randomSet(0, len(data['T'])-1, 5):
        verifyDateFormat(data['T'][_][0])
    # verifyDateFormat(data['T'][0][0])

    if 'PRB' not in data:
        data['PRB'] = list([] for _ in range(len(data['X'])))
        print('No prb data, set to [[]..]. ZONE=%s, testName=%s' % (zone.name, testName))

    someCellNames = list(str(data['C'][_][0]) for _ in randomSet(0, len(data['C'])-1, 5))
    verifiedZone = VerifyZone(zone, someCellNames).zone
    if zone != verifiedZone:
        raise Exception('Test Data for %s has cells from %s!' % (zone.name, verifiedZone.name))

    ptest = PTest()
    ptest.zone = zone
    ptest.run_by = user
    ptest.info['name'] = testName
    ptest.save()

    ptest.info['count'] = shredCell(zone, ptest, data)
    ptest.save()
    return ptest


def proc(ptest, CF_per_band_obj):
    """
    reserved
    """


class CFAddressPerBand:

    class sub:
        CFs = None
        CFc = None

    def __init__(self, zone):
        self.zone = zone
        self._proc()

    def _proc(self):

        band_value = {bv[1]: bv[0] for bv in bTypes}

        zone_CFs = CFunction.objects.filter(zone=self.zone)

        band_CF = []
        band_no_CF = []
        for band in self.zone.data['regrexp']:
            try:
                sub = CFAddressPerBand.sub()
                sub.CFs = zone_CFs.filter(pType='PUSCH', bType=band).last().getMethod()
                sub.CFc = zone_CFs.filter(pType='PUCCH', bType=band).last().getMethod()
                setattr(self, band, sub)
                band_CF.append(band)
            except:
                band_no_CF.append(band)
        for lack_band in band_no_CF:

            lack_band_value = band_value[lack_band]
            min_delta = None
            closest_band = None
            for band in band_CF:
                value = band_value[band]
                delta = abs(lack_band_value - value)
                if not min_delta or min_delta > delta:
                    min_delta = delta
                    closest_band = band
            setattr(self, lack_band, getattr(self, closest_band))

        if not len(band_CF):
            raise CFunction.DoesNotExist('there is not 2 cfs for at least one band')
        self.unknown = getattr(self, band)


def toProc(ptest, CF_per_band):
    try:
        proc(ptest, CF_per_band)
    except Exception as e:
        ptest.info['error'] = e
        ptest.save()
    user = ptest.run_by
    subject = 'PimThor Test #%s is complete' % ptest.id
    message = '%s\nowner: %s' % ('\n'.join(list('%s: %s' % (k, v) for k, v in ptest.info.items())), user.username)
    recipient_list = [user.email]

    sendMail(subject=subject, message=message, recipient_list=recipient_list)


# from .models import OneObj
# # for scheduling
# def main(user, zone, filepaths, testName, prb):
#
#     for rType in rTypes:
#         if not zone.cfunction_set.filter(pType=rType[1]).exists():
#             raise CFunction.DoesNotExist('there is not 2 cfs for at least one band')
#     ptest = CreateTestData(user, zone, filepaths, testName, prb)
#     OneObj.addPTest(ptest.id)


def main(user, zone, filepaths, testName, prb):
    """
    getting CFs, this will be improved later,
    """

    CF_per_band = CFAddressPerBand(zone)

    #   divide into cells
    ptest = CreateTestData(user, zone, filepaths, testName, prb)
    # ADD ERROR TRY EXCEPT!!

    #   analyze data per cell
    t = Thread(target=toProc, args=(ptest, CF_per_band))
    t.start()
