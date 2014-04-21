from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
from Products.DataCollector.DeviceProxy import DeviceProxy
from Products.ZenUtils.ZenScriptBase import ZenScriptBase


class Check_NRPE(PythonPlugin):
    relname = 'nrpeComponent'
    modname = 'ZenPacks.Secure24.Check_NRPE.nrpeComponent'
    compname = 'os'

    # Define default check_nrpe checks used by Secure-24
    # These checks will be added to the device.
    def collect(self, device, log):

        nrpeCmdTableMaps = {}
        nrpeCmdTableMaps["Physical Memory Usage"] = {
            'device_os': "windows",
            'nrpe_cmd': 'CheckMem',
            'nrpe_args': 'ShowAll type=physical',
            'nrpe_timeout': 30,
            }

        nrpeCmdTableMaps["CPU Usage"] = {
            'device_os': "windows",
            'nrpe_cmd': 'CheckCPU',
            'nrpe_args': 'time=5m',
            'nrpe_timeout': 30,
            }

        nrpeCmdTableMaps["DNS Lookups"] = {
            'device_os': "linux",
            'nrpe_cmd': 'check_dns_lookups',
            'nrpe_args': None,
            'nrpe_timeout': 30,
            }

        nrpeCmdTableMaps["Read Only Mounts"] = {
            'device_os': "linux",
            'nrpe_cmd': 'nrpe-check-ro-mounts',
            'nrpe_args': None,
            'nrpe_timeout': 30,
            }

        nrpeCmdTableMaps["LDAP Connectivity"] = {
            'device_os': "linux",
            'nrpe_cmd': 'check_ldap_lookups',
            'nrpe_args': None,
            'nrpe_timeout': 30,
            }

        nrpeCmdTableMaps["NTP Offset"] = {
            'device_os': "linux",
            'nrpe_cmd': 'check_ntp_offset',
            'nrpe_args': None,
            'nrpe_timeout': 60,
            }

        try:
            zsb = ZenScriptBase(self, connect=True)
            dmd_device = zsb.dmd.Devices.findDevice(device.id)
        except:
            log.warn('Unable to pull previous NRPE Components')

        dmd_device_os = str(dmd_device.getDeviceClassName()).lower()
        dmd_device_nrpeComponents = dmd_device.os.nrpeComponent()

        for cmd in dmd_device_nrpeComponents:
            if "linux" in dmd_device_os:
                device_os = "linux"
            elif "windows" in dmd_device_os:
                device_os = "windows"
            else:
                device_os = "unknown"
                log.warn('Unable to determine OS. Skipping...')

            nrpeCmdTableMaps[cmd.id] = {
                'device_os': device_os,
                'nrpe_cmd': cmd.nrpe_cmd,
                'nrpe_args': cmd.nrpe_args,
                'nrpe_timeout': cmd.nrpe_timeout,
                }

        data = {}
        for cmd_index in nrpeCmdTableMaps:
            if nrpeCmdTableMaps[cmd_index]['device_os'] != device_os:
                continue
            else:
                data[cmd_index] = nrpeCmdTableMaps[cmd_index]

        return data


    def process(self, device, results, log):
        rm = self.relMap()
        for cmd_index in results:
            om = self.objectMap()
            om.id = cmd_index
            om.title = cmd_index
            om.device_os = results[cmd_index]['device_os']
            om.nrpe_cmd = results[cmd_index]['nrpe_cmd']
            om.nrpe_args = results[cmd_index]['nrpe_args']
            om.nrpe_timeout = results[cmd_index]['nrpe_timeout']

            rm.append(om)

        return rm
