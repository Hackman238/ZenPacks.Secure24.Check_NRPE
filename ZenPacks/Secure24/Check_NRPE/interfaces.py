from Products.Zuul.form import schema
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.utils import ZuulMessageFactory as _t

class InrpeComponentInfo(IComponentInfo):
    title = schema.TextLine(title=_t(u"Title"))
    nrpe_cmd = schema.TextLine(title=_t(u"Command"))
    nrpe_args = schema.TextLine(title=_t(u"Arguments"))
    nrpe_timeout = schema.Int(title=_t(u"Timeout"))
    nrpe_min = schema.Int(title=_t(u"Min Threshold"))
    nrpe_max = schema.Int(title=_t(u"Max Threshold"))
    nrpe_type = schema.Int(title=_t(u"Check type"))
