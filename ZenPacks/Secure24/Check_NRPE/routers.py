from Products.ZenUtils.Ext import DirectRouter, DirectResponse
from Products import Zuul

class nrpeComponentRouter(DirectRouter):
    def _getFacade(self):
        return Zuul.getFacade('nrpeComponent', self.context)

    def addnrpeComponent(self, title, nrpe_cmd, nrpe_args, nrpe_timeout, userCreated=None, REQUEST=None):
        facade = self._getFacade()
        success, message = facade.addnrpComponent(
            self, title, nrpe_cmd, nrpe_args, nrpe_timeout, userCreated=None, REQUEST=None)
        
        if success:
            return DirectResponse.succeed(message)
        else:
            return DirectResponse.fail(message)
