from home3.models import CellData, Roof
import numpy


def harqConvert(_g, _k):
    """
    reserved
    """


def roundValue(_g, _k):
    try:
        return round(_g[_k][0], 2)
    except TypeError:
        return 0


class EachFun:

    eachFun = {
        'Q16': "reserved",
        'PSK': "reserved",
        'PRB': "reserved",
        'X': "reserved",
        'Ys': "reserved",
        'Yc': "reserved",
        'Ss': "reserved",
        'Sc': "reserved",
        'others': "reserved",
    }


def shredCell(zoneObj, TestObj, DATA, nan_to_zero=True):

    HUGE = {}   # add memory controller and saving fn to DB
    # C = { T : [X, Ys, Yc, Q16, PSK, Sc, Ss, PRB]
    l = len(DATA['C'])
    for i in range(l):

        g = {}
        for key in DATA:
            g[key] = DATA[key][i]
            try:
                g[key] = EachFun.eachFun[key](g, key)
            except KeyError:
                g[key] = EachFun.eachFun['others'](g, key)

        cell = g.pop('C')
        time = g.pop('T')
        try:
            HUGE[cell][time] = g
        except KeyError:
            HUGE[cell] = {time: g}

    for cell, cellData in HUGE.items():

        try:
            cellroof = Roof.objects.get(zone=zoneObj, name=cell)
        except Roof.DoesNotExist:
            cellroof = Roof()
            cellroof.zone = zoneObj
            cellroof.name = cell
            cellroof.save()

        sd = CellData()
        sd.zone = zoneObj
        sd.ptest = TestObj
        sd.roof = cellroof
        sd.name = cell

        #   Narrow PRBs from right to left
        for time in cellData:
            timeprbData = cellData[time]['PRB']
            if nan_to_zero:
                timeprbData = numpy.nan_to_num(timeprbData)
            k = len(timeprbData)-1
            while k >= 0:    # len(timeprbData):
                if not float(timeprbData[k]):   # remove even if it is 0
                    k -= 1  # timeprbData.pop()
                else:
                    break
            if k != len(timeprbData)-1:
                cellData[time]['PRB'] = timeprbData[:k+1]
        sd.data = cellData

        band_type = zoneObj.findBandType(cell)
        if not band_type:
            band_type = 'unknown'
        sd.bType = band_type

        sd.save()

    return len(HUGE)
