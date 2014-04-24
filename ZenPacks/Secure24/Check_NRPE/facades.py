import logging
#log = logging.getLogger('zen.OpenStackFacade')

from zope.interface import implements

from Products.Zuul.facades import ZuulFacade
from Products.Zuul.utils import ZuulMessageFactory as _t

from ZenPacks.Secure24.Check_NRPE.interfaces import InrpeComponentFacade


class nrpeComponentFacade(ZuulFacade):
    implements(InrpeComponentFacade)

    def addnrpeComponent(self, title, nrpe_cmd, nrpe_args, nrpe_timeout, userCreated=None, REQUEST=None):
        """ Adds NRPE Check/Component monitor """

        nrpecomponent = nrpeComponent(title)
        nrpecomponent.nrpe_cmd = nrpe_cmd
        nrpecomponent.nrpe_args = nrpe_args
        nrpecomponent.nrpe_timeout = int(nrpe_timeout)

        if userCreated: nrpecomponent.setUserCreateFlag()

        url = None
        if REQUEST is not None:
            url = self.device().os.absolute_url()

        for nrpeCheck in d.os.nrpeComponent():
            if nrpeCheck.title == nrpecomponent.title:
                return False, _t("A NRPE Check %s already exists." % nrpecomponent.title)
        self.getPrimaryParent().os._setObject(nrpecomponent)

        eventDict = {
            'eventClass': Change_Add,
            'device': self.device().id,
            'component': nrpecomponent or '',
            'summary': 'Added by user: %s' % 'user',
            'severity': Event.Info,
            }
        self.dmd.ZenEventManager.sendEvent(eventDict)

        if REQUEST is not None:
            REQUEST['RESPONSE'].redirect(url)

        return True, _t("NRPE Check %s added." % nrpecomponent.title)
