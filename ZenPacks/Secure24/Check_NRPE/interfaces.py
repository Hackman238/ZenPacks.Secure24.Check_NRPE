from Products.Zuul.form import schema
from Products.Zuul.interfaces.device import IDeviceInfo
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.interfaces import IFacade

# ZuulMessageFactory is the translation layer. You will see strings intended to
# been seen in the web interface wrapped in _t(). This is so that these strings
# can be automatically translated to other languages.
from Products.Zuul.utils import ZuulMessageFactory as _t

class InrpeDeviceInfo(IDeviceInfo):
    nrpe_check_count = schema.Int(title=_t('Number of NRPE Checks'))

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

    def manage_addComponent(self, title, nrpe_cmd, nrpe_args, nrpe_timeout, nrpe_min, nrpe_max, nrpe_graphpoint):
        """ add NRPE Check/Component to device
        """
