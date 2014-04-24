(function(){
 
var router = Zenoss.remote.ComponentRouter;

// Setup Add Dialog Window
Ext.define('Zenoss.component.add.nrpeComponent',{
    extend: 'Zenoss.SmartFormDialog',
    constructor: function(config) {
        config = config || {};
        Ext.applyIf(config, {
            height: 350,
            title: _t('Add NRPE Check...'),
            submitHandler: Ext.bind(this.createnrpeComponent, this),
                items: [{
                    xtype: 'hidden',
                    name: 'userCreated',
                    value: true
                },
		{
                    fieldLabel: 'Title',
                    allowBlank: 'false',
                    name: 'title',
                    width: 260,
                    id: 'titleField',
                    xtype: 'textfield'
		},
		{
                    fieldLabel: 'NRPE Command',
                    allowBlank: 'false',
                    name: 'nrpe_cmd',
                    width: 260,
                    id: 'nrpe_cmdField',
                    xtype: 'textfield'
		},
		{
                    fieldLabel: 'NRPE Arguments',
                    allowBlank: 'true',
                    name: 'nrpe_args',
                    width: 260,
                    id: 'nrpe_argsField',
                    xtype: 'textfield'
		},
		{
                    fieldLabel: 'NRPE Timeout',
                    allowBlank: 'false',
                    name: 'nrpe_timeout',
                    width: 260,
                    id: 'nrpe_timeoutField',
                    value: 30,
                    xtype: 'numberfield',
                    minValue: 10,
                    maxValue: 60
		}]
            });
        this.callParent([config]);
    },
    createnrpeComponent: function(values) {
        values.uid = this.uid;
        router.nrpeComponentRouter.addnrpeComponent(values, function(response){
            if (response.success) {
                Zenoss.message.info(_t("Added NRPE Check"));
            }
        });
    }
});

// Does something
function addnrpeComponentHandler(item) {
    var win = Ext.create('Zenoss.component.add.' + item.dialogId, {
        componentType: item.dialogId,
        uid: Zenoss.env.device_uid
    });
    win.show();
    win.on('destroy', function(){
        refreshComponentTreeAndGrid(win.componentType);
    });
}

// Add menu to Component Add Menu (Lower left hand corner) 
Ext.onReady(function(){
 
    var COMPONENT_ADD_MENU = 'component-add-menu';
    Ext.ComponentMgr.onAvailable(COMPONENT_ADD_MENU, function() {
        var menu = Ext.getCmp(COMPONENT_ADD_MENU);
 
        menu.menuItems.push({
            text: _t('Add NRPE Check'),
            dialogId: 'nrpeComponent',
            handler: addnrpeComponentHandler});
    });
 
});
 
}());
