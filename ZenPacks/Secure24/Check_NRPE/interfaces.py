from Products.Zuul.form import schema
from Products.Zuul.interfaces import IFacade
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.utils import ZuulMessageFactory as _t

class InrpeComponentInfo(IComponentInfo):
    title = schema.TextLine(title=_t(u"Title"))
    nrpe_cmd = schema.TextLine(title=_t(u"Command"))
    nrpe_args = schema.TextLine(title=_t(u"Arguments"))
    nrpe_timeout = schema.Int(title=_t(u"Timeout"))
    nrpe_min = schema.Int(title=_t(u"Min Threshold"))
    nrpe_max = schema.Int(title=_t(u"Max Threshold"))
    device_os = schema.TextLine(title=_t(u"Device OS"))
    nrpe_graphpoint = schema.TextLine(title=_t(u"Graph Point"))

class InrpeComponentFacade(IFacade):
    def addnrpeComponent(self, title, nrpe_cmd, nrpe_args, nrpe_timeout, userCreated=None, REQUEST=None):
        """
        Add NRPE Check.
        """
