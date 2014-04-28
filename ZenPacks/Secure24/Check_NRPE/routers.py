from Products.ZenUtils.Ext import DirectRouter, DirectResponse
from Products import Zuul

class nrpeComponentRouter(DirectRouter):

    def addnrpeComponent(self, title, nrpe_cmd, nrpe_args, nrpe_timeout, nrpe_min, nrpe_max, nrpe_type, userCreated=None, REQUEST=None):
        """ Adds NRPE Check/Component monitor """

        title = prepId(title)
        nrpecomponent = nrpeComponent(title)
        nrpecomponent.nrpe_cmd = nrpe_cmd
        nrpecomponent.nrpe_args = nrpe_args
        nrpecomponent.nrpe_timeout = int(nrpe_timeout)
        nrpecomponent.nrpe_min = nrpe_min
        nrpecomponent.nrpe_max = nrpe_max
        nrpecomponent.nrpe_type = nrpe_type
        nrpecomponent.lockFromDeletion()

        for nrpeCheck in d.os.nrpeComponent():
            if nrpeCheck.title == nrpecomponent.title:
                return DirectResponse.fail(_t("A NRPE Check %s already exists." % nrpecomponent.title))
        self.context.os._setObject(nrpecomponent.id, nrpecomponent)

        _zNRPEChecks = self.context.zNRPEChecks

        nrpe_dict = "{ 'title': '%s', 'cmd': '%s', 'args': %s , 'timeout': %d, 'min': %d, 'max': %d, 'type': '%s' }" \
            % (prepId(title), nrpe_cmd, nrpe_args, int(nrpe_timeout), nrpe_min, nrpe_max, nrpe_type)

        _zNRPEChecks.append(nrpe_dict)        

        eventDict = {
            'eventClass': Change_Add,
            'device': self.device().id,
            'component': nrpecomponent or '',
            'summary': 'Added by user: %s' % 'user',
            'severity': Event.Info,
            }
        self.dmd.ZenEventManager.sendEvent(eventDict)

        return DirectResponse.succeed(_t("NRPE Check %s added." % nrpecomponent.title))

