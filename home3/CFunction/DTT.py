from .proc import CCFs, FilterDataByDistance
from .ML import rTypes


def NewCFunctionsFullData(X, Ys, Yc, nice, zoneObj, bandType, sourceInfo):

    assert len(rTypes) == 2, 'rTypes mismatched'

    Xc = Xs = X
    if not nice:
        Xs, Ys = FilterDataByDistance(X, Ys)
        Xc, Yc = FilterDataByDistance(X, Yc)

    CCFs(
        niceX=Xs,
        niceY=Ys,
        zone=zoneObj,
        ptype=rTypes[0][1],
        btype=bandType,
        sourceInfo=sourceInfo
    )

    CCFs(
        niceX=Xc,
        niceY=Yc,
        zone=zoneObj,
        ptype=rTypes[1][1],
        btype=bandType,
        sourceInfo=sourceInfo
    )