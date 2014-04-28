from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenRelations.zPropertyCategory import setzPropertyCategory

from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.ZenModel.OperatingSystem import OperatingSystem
from Products.ZenModel.Software import Software

import Globals

productNames = (
    'nrpeComponent',
    )

__doc__ = "Secure-24 NRPE Check ZenPack"

ZENPACK_NAME = 'ZenPacks.Secure24.Check_NRPE'

DEVTYPE_NAME = 'Check NRPE'
DEVTYPE_PROTOCOL = 'NRPE'

# Device classes to apply modelers to.
_DEVICE_CLASSES = [
    '/Server/Linux',
    '/Server/Windows',
    ]

# Modelers
_MODELERS = [
    'Secure24.nrpe.Check_NRPE',
    ]

# Setup zProperties
_PACK_Z_PROPS = [
    ('zNRPEChecks', '', 'lines'),
    ]

for name, default_value, type_ in _PACK_Z_PROPS:
    setzPropertyCategory(name, 'NRPE')

# Setup relationship
OperatingSystem._relations += (
    ("nrpeComponent", ToManyCont(ToOne, "ZenPacks.Secure24.Check_NRPE.nrpeComponent", "os")),
)

class ZenPack(ZenPackBase):

    packZProperties = [
        ('zNRPEChecks', '', 'lines'),
        ]

    def install(self, app):

        super(ZenPack, self).install(app)

        for _DEVICE_CLASS in _DEVICE_CLASSES:
            _org = app.zport.dmd.Devices.getOrganizer(_DEVICE_CLASS)
            _modelers = _org.zCollectorPlugins
            _modelers.extend(_MODELERS)
            _org.setZenProperty('zCollectorPlugins', _modelers)

    def remove(self, app, leaveObjects=False):
        for _DEVICE_CLASS in _DEVICE_CLASSES:
            _org = app.zport.dmd.Devices.getOrganizer(_DEVICE_CLASS)
            _modelers = _org.zCollectorPlugins
            for _MODELER in _MODELERS:
                if _MODELER in _modelers:
                    _modelers.remove(_MODELER)
                    _org.setZenProperty('zCollectorPlugins', _modelers)



def onCollectorInstalled(ob, event):
    zpFriendly = 'Secure-24 Check NRPE ZenPack'
    errormsg = '{0} binary cannot be found on {1}. This is part of the nagios-plugins ' + \
               'dependency, and must be installed before {2} can function.'
    
    verifyBin = 'check_nrpe'
    code, output = ob.executeCommand('zenbincheck %s' % verifyBin, 'zenoss', needsZenHome=True)
    if code:
        log.warn(errormsg.format(verifyBin, ob.hostname, zpFriendly))
