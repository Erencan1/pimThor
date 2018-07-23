"""
FRMT is used to create regression expressions for zones. When cell name is search,
these expressions will be used in order to search in correct zone.

n = CommonCharacterBasedLength()

n.add_name('xxxxxx')
n.add_name('xxxxyx')
n.add_name('xxaxxa')

FormatMap is to separate NameFormats by size(length). Same size names will belong to their NameFormats.
However, grouping can be applied. (ABC55, ABC565 -> [A][B][C][5-6]{2,3}
"""


class CommonCharacterBasedLength(dict):

    def __init__(self, chlimit=6, intlimit=3):

        self.chlimit = chlimit
        self.intlimit = intlimit
        super(CommonCharacterBasedLength, self).__init__()

    def add_name(self, newName):

        l = len(newName)
        try:
            frmt = self[l]
        except KeyError:
            self[l] = CommonCharacter()
            frmt = self[l]

        frmt.stage(newName)

    def convert_to_regex(self):
        regr = {}
        for l, obj in self.items():
            regr[l] = obj.convert_to_regex(self.chlimit, self.intlimit)
        return regr


class CommonCharacter(dict):

    def stage(self, cn):

        hash_cn = {}
        for i, h in enumerate(cn):
            try:
                h = int(h)
            except:
                pass
            hash_cn[i] = h

        if not len(self):
            for k, v in hash_cn.items():
                self[k] = {v}
            return

        for index_to_remove in range(len(hash_cn), len(self)):
            del self[index_to_remove]

        for index, ch_set in self.items():

            if hash_cn[index] not in ch_set:
                ch_set.add(hash_cn[index])

    def convert_to_regex(self, chlimit=3, intlimit=3):

        regr = ['^']

        for index in range(len(self)):

            ch_set = self[index]

            contain_int = any(type(ch) == int for ch in ch_set)
            contain_str = any(type(ch) == str for ch in ch_set)

            if contain_int and contain_str:
                regr.append('.?')
            elif contain_int and len(ch_set) > intlimit:
                regr.append('[0-9]')
            elif contain_str and len(ch_set) > chlimit:
                regr.append('[^0-9]')
            else:
                try:
                    regr.append('[%s]' % ','.join(ch_set))
                except:
                    regr.append('[%s]' % ','.join(list(str(ch) for ch in ch_set)))

        regr.append('$')
        return ''.join(regr)