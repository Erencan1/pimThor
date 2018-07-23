# #from .ElasticNet import EN
# #from .Logistic import Logistic
# #from .GradientBoosting import GradientR
# from .AdaBoost import AdaBoostR
# from .Bagging import BaggingR
# #from .Bagging import BaggingC
# #from .Lasso import LSS
# #from .Logistic import Logistic
# #from .Polynomial import Polynomial
# #from .Ridge import Rdg
# ##from .SVR import VectorR
# #from .Linear import Linear
# #from .SGD import SGDR, SGDC
# #from .LDA import LDA
# #from .Tree import DTreeC, DTreeR, ETreeR
# #from .RandomForest import RFR
# #from .KNeighbors import KNR
# #from .ABR_LI import ABR_LI
from .ABR_LI_2 import ABR_LI_2
# #from .KarnelRidge import KernelRdg


mLs = (
    ABR_LI_2,
)
mLs_list = list(ml.name for ml in mLs)

"""
rTypes used for:
    models.CFunction
    NewCFunctions which is removed, and replaced with NewCFunctionsFullData.
    NewCFunctionsFullData is not using rTypes yet has assert len(rTypes) == 2.
Update:
    NewCFunctionsFullData uses rTypes as in order. First is Ys, second is Yc
Ys, Yc:
    CategorizeColumns.CategorizeColumns.features
"""

rTypes = (
    (0, 'PUSCH'),   # Ys
    (1, 'PUCCH'),   # Yc
)


# CFNames = tuple((i, v) for i, v in enumerate(map(lambda x, y: '%s-%s' % (x.name, y), mLs, rType)))


#   bTypes is band types. In (Band Value, 'Band Name'), Band Value is numeric value to use
#   to choose a CF of closeted band (closeted number/Band Value)
#   if there is not a registered cf for that band
bTypes = (
    (700, '700'),
    (1800, '1800'),
    (2100, '2100'),
)