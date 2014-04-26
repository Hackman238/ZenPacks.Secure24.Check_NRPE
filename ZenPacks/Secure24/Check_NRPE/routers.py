from Products.ZenUtils.Ext import DirectRouter, DirectResponse
from Products import Zuul

class nrpeComponentRouter(DirectRouter):
#    def _getFacade(self):
#        return Zuul.getFacade('nrpeComponent', self.context)

    def addnrpeComponent(self, title, nrpe_cmd, nrpe_args, nrpe_timeout, nrpe_min, nrpe_max, nrpe_type, userCreated=None, REQUEST=None):
#        facade = self._getFacade()
#        success, message = facade.addnrpComponent(
#            self, title, nrpe_cmd, nrpe_args, nrpe_timeout, userCreated=None, REQUEST=None)
        
#        if success:
#            return DirectResponse.succeed(message)
#        else:
#            return DirectResponse.fail(message)

        """ Adds NRPE Check/Component monitor """
        title = prepId(title)
        nrpecomponent = nrpeComponent(title)
        nrpecomponent.nrpe_cmd = nrpe_cmd
        nrpecomponent.nrpe_args = nrpe_args
        nrpecomponent.nrpe_timeout = int(nrpe_timeout)
        nrpecomponent.nrpe_min = int(nrpe_min)
        nrpecomponent.nrpe_max = int(nrpe_max)
        nrpecomponent.nrpe_type = nrpe_type
        nrpecomponent.lockFromDeletion()

        if userCreated: nrpecomponent.setUserCreateFlag()

#        url = None
#        if REQUEST is not None:
#            url = self.device().os.absolute_url()

        for nrpeCheck in d.os.nrpeComponent():
            if nrpeCheck.title == nrpecomponent.title:
                return DirectResponse.fail(_t("A NRPE Check %s already exists." % nrpecomponent.title))
        self.context.os._setObject(nrpecomponent.id, nrpecomponent)
        
        eventDict = {
            'eventClass': Change_Add,
            'device': self.device().id,
            'component': nrpecomponent or '',
            'summary': 'Added by user: %s' % 'user',
            'severity': Event.Info,
            }
        self.dmd.ZenEventManager.sendEvent(eventDict)

#        if REQUEST is not None:
#            REQUEST['RESPONSE'].redirect(url)

        return DirectResponse.succeed(_t("NRPE Check %s added." % nrpecomponent.title))

#        if success:
#            return DirectResponse.succeed(message)
#        else:
#            return DirectResponse.fail(message)

