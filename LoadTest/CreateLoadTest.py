from LoadTest.CategorizeColumn import LoadColumns
from General.single.the_dict import TheDict
from LoadTest.models import CellLoadData, NodeLoad, RoofLoad, LoadTest, LoadUser
import os


#   verify date format


def create_load_test_proc(filepaths, user):

    data = LoadColumns(filepaths, prb=True).FileData
    data = {k: v.values for k, v in data.items()}

    T = data['T']
    N = data['N']
    C = data['C']
    D = data['D']
    Ys = data['Ys']
    Yc = data['Yc']
    RF = data['RF']
    PRB = data['PRB']

    node_data = {}
    l = len(T)
    for i in range(l):

        n, c, t, ys, yc, d, r, p = N[i][0], C[i][0], T[i][0], Ys[i][0], Yc[i][0], D[i][0], RF[i], PRB[i]

        if any(str(u) in ['', 'nan'] for u in (n, c, t)) or all(str(u) in ['', 'nan'] for u in (ys, yc, d, r, p)):
            continue

        row = {
            'Ys': ys,
            'Yc': yc,
            'D': d,
            'PRB': p
        }
        for i, rv in enumerate(r, 1):
            row['RF%s' % i] = rv

        for k, v in row.items():
            TheDict.insert(
                node_data,
                n,
                c,
                k,
                t,
                v
            )

    load_test = LoadTest()
    load_test.run_by = LoadUser(user)
    load_test.save()

    load_test_data = {}

    for nodeName, nodeData in node_data.items():
        try:
            node = NodeLoad.objects.get(name=nodeName)
        except NodeLoad.DoesNotExist:
            node = NodeLoad()
            node.name = nodeName
            node.save()
        load_test_data[nodeName] = {}
        for cellName, cellData in nodeData.items():
            try:
                roof = node.roofload_set.get(name=cellName)
            except RoofLoad.DoesNotExist:
                roof = RoofLoad()
                roof.node = node
                roof.name = cellName
                roof.save()
            cell = CellLoadData()
            cell.test = load_test
            cell.roof = roof
            cell.name = cellName
            cell.data = cellData
            cell.save()
            load_test_data[nodeName][cellName] = cell.id

    load_test.data = load_test_data
    load_test.save(update_fields=['data'])



def create_load_test(filepaths, user):
    try:
        create_load_test_proc(filepaths, user)
    except Exception as e:
        for filepath in filepaths:
            os.remove(filepath)
        raise ProcessLookupError(
            'During reading csv files\nError is caused by %s\nCSV file(s) must have below columns:\n'
            '' % e
        )