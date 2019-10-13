__author__       = "David Kalliecharan"
__author_email__ = "david@david.science"
__license__      = "ISC"

try:
    from .xps import *
    from . import parser
    from . import sfwagner
    from . import scatter

    # populate Wagner sensitivity factors for convienence
    sf = sfwagner.SensitivityFactors()
except ImportError as err:
    print(err)
    pass
