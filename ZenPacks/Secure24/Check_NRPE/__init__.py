productNames = (
    'nrpeComponent',
    )

from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.ZenModel.Device import Device
from Products.ZenModel.Software import Software
from Products.ZenModel.OperatingSystem import OperatingSystem
#Device._relations += (('nrpeComponent', ToManyCont(ToOne,'ZenPacks.Secure-24.Check_NRPE.nrpeComponent','os')),)
_relations = Software._relations + (
    ("nrpeComponent", ToManyCont(ToOne, "ZenPacks.Secure-24.Check_NRPE.nrpeComponent", "os")),
)

