import os,re
import logging
log = logging.getLogger('zen.nrpeComponentfacade')

from zope.interface import implements
from Products.Zuul.facades import ZuulFacade
from Products.Zuul.utils import ZuulMessageFactory as _t
from ZenPacks.Secure24.Check_NRPE.nrpeComponent import nrpeComponent
from ZenPacks.Secure24.Check_NRPE.interfaces import InrpeComponentFacade


class nrpeComponentFacade(ZuulFacade):
    implements(InrpeComponentFacade)

    def addNrpeComponent(self, title, nrpe_cmd, nrpe_args, nrpe_timeout, nrpe_min, nrpe_max, nrpe_graphpoint): 
        """ Adds NRPE Check/Component monitor"""
        id = title
        nrpecomponent = nrpeComponent(id)
        title.nrpeComponents._setObject(nrpecomponent.id, nrpecomponent)
        nrpecomponent = title.nrpeComponents._getOb(nrpecomponent.id)
        nrpecomponent.nrpe_cmd = nrpe_cmd 
        nrpecomponent.nrpe_args = nrpe_args
        nrpecomponent.nrpe_timeout = nrpe_timeout
        nrpecomponent.nrpe_min = nrpe_min
        nrpecomponent.nrpe_max = nrpe_max
        nrpecomponent.nrpe_graphpoint = nrpe_graphpoint

        return True, _t(" Added NRPE Check for device %s" % (ob.id))
