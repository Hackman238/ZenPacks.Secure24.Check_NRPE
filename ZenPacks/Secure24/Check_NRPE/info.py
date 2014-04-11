# This file is the conventional place for "Info" adapters. Info adapters are
# a crucial part of the Zenoss API and therefore the web interface for any
# custom classes delivered by your ZenPack. Examples of custom classes that
# will almost certainly need info adapters include datasources, custom device
# classes and custom device component classes.

# Mappings of interfaces (interfaces.py) to concrete classes and the factory
# (these info adapter classes) used to create info objects for them are managed
# in the configure.zcml file.

from zope.interface import implements

from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.device import DeviceInfo
from Products.Zuul.infos.component import ComponentInfo

from ZenPacks.Secure24.Check_NRPE.interfaces import InrpeComponentInfo 


class nrpeComponentInfo(ComponentInfo):
    implements(InrpeComponentInfo)

    title = ProxyProperty("title")
    nrpe_cmd = ProxyProperty("nrpe_cmd")
    nrpe_args = ProxyProperty("nrpe_args")
    nrpe_timeout = ProxyProperty("nrpe_timeout")
    nrpe_min = ProxyProperty("nrpe_min")
    nrpe_max = ProxyProperty("nrpe_max")
    device_os = ProxyProperty("device_os")
    nrpe_graphpoint = ProxyProperty("nrpe_graphpoint")

