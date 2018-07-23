#   It categorizes columns according to keywords
import pandas as pd


class CategorizeColumns:

    features = {
        ('reserved')                            :   ('T', 0),
        ('reserved')                            :   ('C', 0),
        ('reserved')                            :   ('X', 0),
        ('reserved')                            :   ('X', 1),
        ('reserved')                            :   ('X', 2),
        ('reserved')                            :   ('Ys', 0),
        ('reserved')                            :   ('Yc', 0),
        ('reserved', 'reserved', 'reserved')    :   ('Q16', 1),
        ('reserved', 'reserved', 'reserved')    :   ('Q16', 0),
        ('reserved', 'reserved', 'reserved')    :   ('PSK', 1),
        ('reserved', 'reserved', 'reserved')    :   ('PSK', 0),
        ('reserved', 'reserved')                :   ('Sc', 0),
        ('reserved', 'reserved')                :   ('Ss', 1),
    }

    def __init__(self, FilePath, prb=False):
        if type(FilePath) is list:
            allData = []
            for fp in FilePath:
                allData.append(pd.read_csv(fp))
            self.FileData = pd.concat(allData)
        else:
            self.FileData = pd.read_csv(FilePath)
        # # self.FileData = self.FileData.dropna(how='all')
        # Add later: remove rows where certain values (USER, PUSCH, ...) are non-numeric
        # self.FileData = self.FileData.dropna(axis=0) how=all
        # self.FileData = self.FileData[pd.to_numeric(self.FileData['PUSCH'], errors='coerce').notnull()]

        self.headers = list(self.FileData.columns)
        if prb:
            self._addprb()
        self.headerWeight = {}
        self.featureWeight = {f: [] for f in self.__class__.features}
        self._headering()
        self._groupXYQ()

    def _addprb(self):

        """
        reserved
        """

    def _headering(self):

        for h in self.headers:
            self.headerWeight[h] = []
            self._hWeight(h)

        for hfs in sorted(self.headerWeight.items(), key=lambda x: len(x[1])):

            h, fs = hfs
            for f in fs:
                if self._pathing(h, f, [h], [f]):
                    for fi in self.headerWeight[h]:
                        self.featureWeight[fi].remove(h)
                    for hi in self.featureWeight[f]:
                        self.headerWeight[hi].remove(f)

    def _hWeight(self, header):

        for feature in self.__class__.features:
            if all(word in header for word in feature):
                self.headerWeight[header].append(feature)
                self.featureWeight[feature].append(header)

    def _pathing(self, parentH, parentF, hroud, froud):

        hs = self.featureWeight[parentF].copy()
        hs.remove(parentH)
        if len(hs):
            for h in hs:
                if h in hroud:
                    continue
                fw = self.headerWeight[h]
                for f in fw:
                    if f in froud:
                        continue
                    if self._pathing(h, f, hroud + [h], froud + [f]):
                        return True
            return False
        else:
            return True

    def _groupXYQ(self):

        groups = {}
        for h, features in self.headerWeight.items():
            if len(features) > 1:
                raise IndexError('Header Issue len > 1; %s: %s' % (h, features))
            elif len(features) == 1:
                feature = features[0]
                groupName = self.__class__.features[feature]
                try:
                    groups[groupName[0]][groupName[1]] = self.headers.index(h)
                except KeyError:
                    groups[groupName[0]] = {groupName[1]: self.headers.index(h)}
        DATA = {}
        for groupName, columns in groups.items():
            clmGroup = []
            for clmid in sorted(columns):
                clmGroup.append(columns[clmid])
            DATA[groupName] = self.FileData.iloc[:, clmGroup]
        self.FileData = DATA
