from Globals import DTMLFile
from Products.ZenModel.OSComponent import OSComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

def manage_addnrpeComponent(context, title, nrpe_cmd, nrpe_args, nrpe_timeout, userCreated=None, REQUEST = None):
    """ Adds NRPE Check/Component monitor"""

    nrpecomponent = nrpeComponent(title)
    nrpecomponent.nrpe_cmd = nrpe_cmd
    nrpecomponent.nrpe_args = nrpe_args
    nrpecomponent.nrpe_timeout = int(nrpe_timeout)
 	
    if userCreated: nrpecomponent.setUserCreateFlag()
 	
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()
                                     +'/manage_main')
	
addnrpeComponent = DTMLFile('dtml/addnrpeComponent',globals())


class nrpeComponent(OSComponent):
    meta_type = portal_type = "nrpeComponent"

    title = None
    nrpe_cmd = None
    nrpe_args = None
    nrpe_timeout = 30
    device_os = None

    _properties = OSComponent._properties + (
        {'id': 'title', 'type': 'string', 'mode': ''},
        {'id': 'nrpe_cmd', 'type': 'string', 'mode': ''},
        {'id': 'nrpe_args', 'type': 'string', 'mode': ''},
        {'id': 'nrpe_timeout', 'type': 'int', 'mode': ''},
        {'id': 'device_os', 'type': 'string', 'mode': ''},
    )

    _relations = OSComponent._relations + (
        ("os", ToOne(ToManyCont,"Products.ZenModel.OperatingSystem","nrpeComponent")),
        )

    isUserCreatedFlag = False
    def isUserCreated(self):
        return self.isUserCreatedFlag

    def getRRDTemplateName(self):
        return 'nrpeComponent'

    def manage_deleteComponent(self, REQUEST=None):
        """
        Delete OSComponent
        """
        url = None
        if REQUEST is not None:
            url = self.device().os.absolute_url()
        self.getPrimaryParent()._delObject(self.id)
        '''
        eventDict = {
            'eventClass': Change_Remove,
            'device': self.device().id,
            'component': self.id or '',
            'summary': 'Deleted by user: %s' % 'user',
            'severity': Event.Info,
            }
        self.dmd.ZenEventManager.sendEvent(eventDict)
        '''
        if REQUEST is not None:
            REQUEST['RESPONSE'].redirect(url)

    def manage_updateComponent(self, datamap, REQUEST=None):
        '''Update OSComponent'''
        url = None
        if REQUEST is not None:
            url = self.device().os.absolute_url()
        self.updateCustomRelations()
        self.getPrimaryParent()._updateObject(self, datamap)
        '''
        eventDict = {
            'eventClass': Change_Set,
            'device': self.device().id,
            'component': self.id or '',
            'summary': 'Updated by user: %s' % 'user',
            'severity': Event.Info,
            }
        self.dmd.ZenEventManager.sendEvent(eventDict)
        '''
        if REQUEST is not None:
            REQUEST['RESPONSE'].redirect(url)
