productNames = (
    'nrpeComponent',
    )

from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.ZenModel.OperatingSystem import OperatingSystem
from Products.ZenModel.Software import Software


OperatingSystem._relations += (
    ("nrpeComponent", ToManyCont(ToOne, "ZenPacks.Secure24.Check_NRPE.nrpeComponent", "os")),
)
