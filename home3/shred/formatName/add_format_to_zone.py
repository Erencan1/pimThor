"""
add_format_to_zone is to define cell name format according to band type.
For the pimthor test, this will be used to define band type of cell.
"""
from .FRMT import CommonCharacterBasedLength


def add_format_to_zone(zone, bandType, cell_name_matrix):

    FM = CommonCharacterBasedLength()

    try:
        regrexp = zone.data['regrexp'][bandType]
    except KeyError:
        zone.data['regrexp'][bandType] = {}
        regrexp = zone.data['regrexp'][bandType]

    for cell_name in cell_name_matrix:
        cell_name = cell_name[0]
        if not zone.validName(cell_name, bandType):
            FM.add_name(cell_name)

    if len(FM):

        for l, regr in FM.convert_to_regex().items():
            print('NEW ~ l=%s, regr=%s' % (l, regr))
            try:
                regrexp[str(l)].append(regr)
            except KeyError:
                regrexp[str(l)] = [regr]

        zone.save()