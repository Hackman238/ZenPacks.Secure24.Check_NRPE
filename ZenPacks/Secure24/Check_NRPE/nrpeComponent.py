from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenRelations.RelSchema import ToManyCont, ToOne


class nrpeComponent(DeviceComponent, ManagedEntity):
    meta_type = portal_type = "nrpeComponent"

    title = None
    nrpe_cmd = None
    nrpe_args = None
    nrpe_timeout = 30
    nrpe_cycle = 5
    nrpe_retries = 3
    

    _properties = ManagedEntity._properties + (
        {'id': 'title', 'type': 'string', 'mode': ''},
        {'id': 'nrpe_cmd', 'type': 'string', 'mode': ''},
        {'id': 'nrpe_args', 'type': 'string', 'mode': ''},
        {'id': 'nrpe_timeout', 'type': 'int', 'mode': ''},
        {'id': 'nrpe_cycle', 'type': 'int', 'mode': ''},
        {'id': 'nrpe_retries', 'type': 'int', 'mode': ''},
    )

    _relations = ManagedEntity._relations + (
        ('nrpeDevice', ToOne(ToManyCont,
            'ZenPacks.Secure24.Check_NRPE.nrpeDevice',
            'nrpeComponents',
            ),
        ),
    )

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

    def getRRDTemplateName(self):
        return 'nrpeComponent'

