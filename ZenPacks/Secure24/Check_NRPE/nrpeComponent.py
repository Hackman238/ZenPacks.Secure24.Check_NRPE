from Products.ZenModel.OSComponent import OSComponent
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.ZenEvents.ZenEventClasses import Change_Add,Change_Remove,Change_Set,Change_Add_Blocked,Change_Remove_Blocked,Change_Set_Blocked

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
        {'id': 'nrpe_min', 'type': 'string', 'mode': ''},
        {'id': 'nrpe_max', 'type': 'string', 'mode': ''},
        {'id': 'nrpe_timeout', 'type': 'int', 'mode': ''},
        {'id': 'device_os', 'type': 'string', 'mode': ''},
        {'id': 'nrpe_type', 'type': 'string', 'mode': ''},
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
        
        eventDict = {
            'eventClass': Change_Remove,
            'device': self.device().id,
            'component': self.id or '',
            'summary': 'Deleted by user: %s' % 'user',
            'severity': Event.Info,
            }
        self.dmd.ZenEventManager.sendEvent(eventDict)
        
        if REQUEST is not None:
            REQUEST['RESPONSE'].redirect(url)

