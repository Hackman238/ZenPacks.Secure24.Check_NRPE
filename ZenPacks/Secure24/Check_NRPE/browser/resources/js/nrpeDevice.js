(function(){

    var ZC = Ext.ns('Zenoss.component');

    ZC.registerName(
        'nrpeComponent',
        _t('NRPE Check'),
        _t('NRPE Checks'));

    Ext.onReady(function() {
        var DEVICE_OVERVIEW_ID = 'deviceoverviewpanel_summary';
        Ext.ComponentMgr.onAvailable(DEVICE_OVERVIEW_ID, function(){
            var overview = Ext.getCmp(DEVICE_OVERVIEW_ID);
            });
        });


    ZC.nrpeComponentPanel = Ext.extend(ZC.ComponentGridPanel, {
        constructor: function(config) {
            config = Ext.applyIf(config||{}, {
                componentType: 'nrpeComponent',
                autoExpandColumn: 'name',
                sortInfo: {
                    field: 'name',
                    direction: 'ASC'
                },
                fields: [
                    {name: 'uid'},
                    {name: 'name'},
                    {name: 'status'},
                    {name: 'severity'},
                    {name: 'usesMonitorAttribute'},
                    {name: 'monitor'},
                    {name: 'monitored'},
                    {name: 'locking'},
                    {name: 'nrpe_cmd'},
                    {name: 'nrpe_args'},
                    {name: 'nrpe_timeout'},
                    {name: 'nrpe_min'},
                    {name: 'nrpe_max'},
                    {name: 'nrpe_graphpoint'}
                ],
                columns: [{
                    id: 'severity',
                    dataIndex: 'severity',
                    header: _t('Events'),
                    renderer: Zenoss.render.severity,
                    sortable: true,
                    width: 50
                },{
                    id: 'name',
                    dataIndex: 'name',
                    header: _t('Name'),
                    sortable: true
                },{
                    id: 'nrpe_cmd',
                    dataIndex: 'nrpe_cmd',
                    header: _t('NRPE Command'),
                    sortable: true,
                    width: 260
                },{
                    id: 'nrpe_args',
                    dataIndex: 'nrpe_args',
                    header: _t('NRPE Command Arguments'),
                    sortable: true,
                    width: 200
                },{
                    id: 'nrpe_graphpoint',
                    dataIndex: 'nrpe_graphpoint',
                    header: _t('Graph Point'),
                    sortable: true,
                    width: 120
                },{
                    id: 'nrpe_timeout',
                    dataIndex: 'nrpe_timeout',
                    header: _t('Timeout'),
                    sortable: true,
                    width: 50
                },{
                    id: 'nrpe_min',
                    dataIndex: 'nrpe_min',
                    header: _t('Min Threshold'),
                    sortable: true,
                    width: 50
                },{
                    id: 'nrpe_max',
                    dataIndex: 'nrpe_max',
                    header: _t('Max Threshold'),
                    sortable: true,
                    width: 50
                },{
                    id: 'monitored',
                    dataIndex: 'monitored',
                    header: _t('Monitored'),
                    renderer: Zenoss.render.checkbox,
                    sortable: true,
                    width: 70
                },{
                    id: 'locking',
                    dataIndex: 'locking',
                    header: _t('Locking'),
                    renderer: Zenoss.render.locking_icons,
                    width: 65
                }]
            });

            ZC.nrpeComponentPanel.superclass.constructor.call(
                this, config);
        }
    });

    Ext.reg('nrpeComponentPanel', ZC.nrpeComponentPanel);

})();
