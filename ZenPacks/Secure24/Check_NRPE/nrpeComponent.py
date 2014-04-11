from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Globals import DTMLFile
from Products.ZenUtils.Utils import prepId


def manage_addnrpeComponent(context, title, nrpe_cmd, nrpe_args, nrpe_timeout, nrpe_min, nrpe_max, nrpe_graphpoint, userCreated=None, REQUEST = None):
    """ Adds NRPE Check/Component monitor"""

    id = prepId(title)
    new_nrpecomponent = nrpeComponent(id)

    context._setObject(id, new_nrpecomponent)

    nrpecomponent = context._getOb(id)

    nrpecomponent.nrpe_cmd = nrpe_cmd
    nrpecomponent.nrpe_args = nrpe_args
    nrpecomponent.nrpe_timeout = int(nrpe_timeout)
    nrpecomponent.nrpe_min = int(nrpe_min)
    nrpecomponent.nrpe_max = int(nrpe_max)
    nrpecomponent.nrpe_graphpoint = nrpe_graphpoint

    if userCreated: nrpecomponent.setUserCreateFlag()

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()
                                     +'/manage_main')
#    return True, _t(" Added NRPE Check for device %s" % (ob.id))

addnrpeComponent = DTMLFile('dtml/addnrpeComponent',globals())


class nrpeComponent(DeviceComponent, ManagedEntity):
    meta_type = portal_type = "nrpeComponent"

    title = None
    nrpe_cmd = None
    nrpe_args = None
    nrpe_timeout = 30
    nrpe_min = 0
    nrpe_max = 0
    device_os = None
    nrpe_graphpoint = None

    _properties = ManagedEntity._properties + (
        {'id': 'title', 'type': 'string', 'mode': ''},
        {'id': 'nrpe_cmd', 'type': 'string', 'mode': ''},
        {'id': 'nrpe_args', 'type': 'string', 'mode': ''},
        {'id': 'nrpe_timeout', 'type': 'int', 'mode': ''},
        {'id': 'nrpe_min', 'type': 'int', 'mode': ''},
        {'id': 'nrpe_max', 'type': 'int', 'mode': ''},
        {'id': 'device_os', 'type': 'string', 'mode': ''},
        {'id': 'nrpe_graphpoint', 'type': 'string', 'mode': ''},
    )

    _relations = ManagedEntity._relations + (
        ('nrpeDevice', ToOne(ToManyCont,
            'ZenPacks.Secure24.Check_NRPE.nrpeDevice',
            'nrpeComponents',
            ),
        ),
    )

#    _relations = ManagedEntity._relations + (
#        ("os", ToOne(ToManyCont,"ZenPacks.Secure24.Check_NRPE.nrpeDevice","nrpeComponents")),
#        )

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
        return self.nrpeDevice()

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

