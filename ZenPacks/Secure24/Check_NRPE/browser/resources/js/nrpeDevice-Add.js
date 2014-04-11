(function(){
    var router = Zenoss.remote.DeviceRouter;

    Ext.define('Zenoss.component.add.nrpeComponent',{
        extend: 'Zenoss.SmartFormDialog',
        constructor: function(config) {
            config = config || {};
            Ext.applyIf(config, {
                height: 250,
                title: _t('Add NRPE Check'),
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
		},
		{
                    fieldLabel: 'NRPE Minimum Threshold Value',
                    allowBlank: 'false',
                    name: 'nrpe_min',
                    width: 260,
                    id: 'nrpe_minField',
                    xtype: 'numberfield'
		},
		{
                    fieldLabel: 'NRPE Maximum Threshold Value',
                    allowBlank: 'false',
                    name: 'nrpe_max',
                    width: 260,
                    id: 'nrpe_maxField',
                    xtype: 'numberfield'
		},
		{
                    fieldLabel: 'Graph Point',
                    allowBlank: 'false',
                    name: 'nrpe_graphpoint',
                    width: 260,
                    id: 'nrpe_graphpointField',
                    xtype: 'textfield',
                    value: 'Errors'
		}]
            });
            this.callParent([config]);
        },
        createnrpeComponent: function(values) {
            values.uid = this.uid;
            router.addnrpeComponent(values, function(response){
                if (response.success) {
                    Zenoss.message.info(_t('Added NRPE Check Entry'));
                }
            });
        }
    });
});
