from Products.ZenModel.OSComponent import OSComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Globals import DTMLFile
from Products.ZenUtils.Utils import prepId


def manage_addnrpeComponent(context, title, nrpe_cmd, nrpe_args, nrpe_timeout, userCreated=None, REQUEST = None):
    """ Adds NRPE Check/Component monitor"""

    id = prepId(title)
    new_nrpecomponent = nrpeComponent(id)

    context._setObject(id, new_nrpecomponent)

    nrpecomponent = context._getOb(id)

    nrpecomponent.nrpe_cmd = nrpe_cmd
    nrpecomponent.nrpe_args = nrpe_args
    nrpecomponent.nrpe_timeout = int(nrpe_timeout)

    if userCreated: nrpecomponent.setUserCreateFlag()

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()
                                     +'/manage_main')

addnrpeComponent = DTMLFile('dtml/addnrpeComponent',globals())


class nrpeComponent(OSComponent, ManagedEntity):
    meta_type = portal_type = "nrpeComponent"

    title = None
    nrpe_cmd = None
    nrpe_args = None
    nrpe_timeout = 30
    device_os = None

    _properties = ManagedEntity._properties + (
        {'id': 'title', 'type': 'string', 'mode': ''},
        {'id': 'nrpe_cmd', 'type': 'string', 'mode': ''},
        {'id': 'nrpe_args', 'type': 'string', 'mode': ''},
        {'id': 'nrpe_timeout', 'type': 'int', 'mode': ''},
        {'id': 'device_os', 'type': 'string', 'mode': ''},
    )


#    _relations = ManagedEntity._relations + (
#        ("os", ToOne(ToManyCont,"Products.ZenModel.OperatingSystem","nrpeComponent")))

    _relations = OSComponent._relations + (
        ("os", ToOne(ToManyCont,"Products.ZenModel.OperatingSystem","nrpeComponent")),
        )

#    _relations = ManagedEntity._relations + (
#        ('nrpeDevice', ToOne(ToManyCont,
#            'ZenPacks.Secure24.Check_NRPE.nrpeDevice',
#            'nrpeComponents',
#            ),
#        ),
#    )


    # Defining the "perfConf" action here causes the "Graphs" display to be
    # available for components of this type.
    factory_type_information = ({
        'actions': ({
            'id': 'perfConf',
            'name': 'Template',
            'action': 'objTemplates',
            'permissions': (ZEN_CHANGE_DEVICE,),
        },),
    },)

    # Custom components must always implement the device method. The method
    # should return the device object that contains the component.
    def device(self):
        return self.getPrimaryParent()

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
        """
        Update OSComponent
        """
        url = None
        if REQUEST is not None:
            url = self.device().os.absolute_url()
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

