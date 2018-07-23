from home3.CategorizeColumn import CategorizeColumns as _CategorizeColumns


LoadColumns = type('LoadColumns', (object,), dict(_CategorizeColumns.__dict__))
LoadColumns.features = {
    ('reserved')                :   ('T', 0),
    ('reserved')                :   ('N', 0),
    ('reserved')                :   ('C', 0),
    ('reserved')                :   ('D', 0),
    ('reserved')                :   ('Ys', 0),
    ('reserved')                :   ('Yc', 0),
    ('reserved', '1')           :   ('RF', 0),
    ('reserved', '2')           :   ('RF', 1),
    ('reserved', '3')           :   ('RF', 2),
    ('reserved', '4')           :   ('RF', 3),
}
