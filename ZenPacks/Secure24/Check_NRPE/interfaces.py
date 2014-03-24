from Products.Zuul.form import schema
from Products.Zuul.interfaces.device import IDeviceInfo
from Products.Zuul.interfaces.component import IComponentInfo

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
    nrpe_cycle = schema.Int(title=_t(u"Cycle Time"))
    nrpe_retries = schema.Int(title=_t(u"Retries"))
