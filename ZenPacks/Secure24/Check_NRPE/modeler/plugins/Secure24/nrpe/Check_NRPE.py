from Products.DataCollector.plugins.CollectorPlugin import (PythonPlugin, CollectorPlugin)
from Products.DataCollector.DeviceProxy import DeviceProxy
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from Products.ZenUtils.Utils import prepId

class Check_NRPE(PythonPlugin):
    relname = 'nrpeComponent'
    modname = 'ZenPacks.Secure24.Check_NRPE.nrpeComponent'
    compname = 'os'

#    deviceProperties = CollectorPlugin.deviceProperties + (
#        'cNRPEChecks',
#        )

    deviceProperties = CollectorPlugin.deviceProperties + (
        'cNRPEChecks',
        )


    def collect(self, device, log):
        nrpe_checks = device.cNRPEChecks
        data = {}

        for check in nrpe_checks:
            nrpe_check = eval(check)
            check_id = prepId(nrpe_check['title'])
            data[check_id] = {
                'id': check_id,
                'nrpe_title': nrpe_check['title'],
                'nrpe_cmd': nrpe_check['cmd'],
                'nrpe_args': nrpe_check['args'],
                'nrpe_min': nrpe_check['min'],
                'nrpe_max': nrpe_check['max'],
                'nrpe_timeout': nrpe_check['timeout'],
                'nrpe_type': nrpe_check['type'],
                }

        return data


    def process(self, device, results, log):
        rm = self.relMap()

        for cmd_index in results:
            om = self.objectMap()
            om.id = cmd_index
            om.title = results[cmd_index]['nrpe_title']
            om.nrpe_cmd = results[cmd_index]['nrpe_cmd']
            om.nrpe_args = results[cmd_index]['nrpe_args']
            om.nrpe_timeout = results[cmd_index]['nrpe_timeout']
            om.nrpe_min = results[cmd_index]['nrpe_min']
            om.nrpe_max = results[cmd_index]['nrpe_max']
            om.nrpe_type = results[cmd_index]['nrpe_type']

            rm.append(om)

        return rm

