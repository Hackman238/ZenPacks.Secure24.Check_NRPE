from Products.DataCollector.plugins.CollectorPlugin import (CollectorPlugin, SnmpPlugin, PythonPlugin, GetTableMap)
from Products.DataCollector.DeviceProxy import DeviceProxy
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
import subprocess
import os


def Get_TotalMemory(SnmpPlugin):
    pass


class Check_NRPE(PythonPlugin):
    relname = 'nrpeComponents'
    modname = 'ZenPacks.Secure24.Check_NRPE.nrpeComponent'


    # Define default check_nrpe checks used by Secure-24
    # These checks will be added to the device.
    def collect(self, device, log):

        snmpGetTableMaps = (
        GetTableMap(
            'total_memory__entry', '.1.3.6.1.2.1.25.2.2', {
                '.0': 'total_memory_index',
                }
            ),
        )


#        mem_instances = snmpGetTableMaps.get('total_memory__entry', {})
#        for snmpindex, row in mem_instances.items():
#            device_mem = row.get('total_memory_index')

#        import pdb; pdb.set_trace()
        device_mem = 8000000
        nrpeCmdTableMaps = {}
        nrpeCmdTableMaps["Physical Memory Usage"] = {
            'device_os': "windows",
            'nrpe_cmd': 'CheckMem',
            'nrpe_args': 'ShowAll type=physical',
            'nrpe_timeout': 30,
            'nrpe_min': 0,
            'nrpe_max': device_mem,
            'nrpe_graphpoint': 'Current Usage'
            }

        nrpeCmdTableMaps["CPU Usage"] = {
            'device_os': "windows",
            'nrpe_cmd': 'CheckCPU',
            'nrpe_args': 'time=5m',
            'nrpe_timeout': 30,
            'nrpe_min': 0,
            'nrpe_max': 99,
            'nrpe_graphpoint': '5m'
            }

        nrpeCmdTableMaps["DNS Lookups"] = {
            'device_os': "linux",
            'nrpe_cmd': 'check_dns_lookups',
            'nrpe_args': None,
            'nrpe_timeout': 30,
            'nrpe_min': 0,
            'nrpe_max': 0,
            'nrpe_graphpoint': 'Errors'
            }

        nrpeCmdTableMaps["Read Only Mounts"] = {
            'device_os': "linux",
            'nrpe_cmd': 'nrpe-check-ro-mounts',
            'nrpe_args': None,
            'nrpe_timeout': 30,
            'nrpe_min': 0,
            'nrpe_max': 0,
            'nrpe_graphpoint': 'Errors'
            }

        nrpeCmdTableMaps["LDAP Connectivity"] = {
            'device_os': "linux",
            'nrpe_cmd': 'check_ldap_lookups',
            'nrpe_args': None,
            'nrpe_timeout': 30,
            'nrpe_min': 0,
            'nrpe_max': 0,
            'nrpe_graphpoint': 'Errors'
            }

        nrpeCmdTableMaps["NTP Offset"] = {
            'device_os': "linux",
            'nrpe_cmd': 'check_ntp_offset',
            'nrpe_args': None,
            'nrpe_timeout': 60,
            'nrpe_min': 0,
            'nrpe_max': 0,
            'nrpe_graphpoint': 'Errors'
            }

        try:
            zsb = ZenScriptBase(self, connect=True)
            dmd_device = zsb.dmd.Devices.findDevice(device.id)
            dmd_device_os = str(dmd_device.getDeviceClassName()).lower()
            dmd_device_nrpeComponents = dmd_device.nrpeComponents()
            for cmd in dmd_device_nrpeComponents:

                 nrpeCmdTableMaps[cmd.id] = {
                     'device_os': cmd.device_os,
                     'nrpe_cmd': cmd.nrpe_cmd,
                     'nrpe_args': cmd.nrpe_args,
                     'nrpe_timeout': cmd.nrpe_timeout,
                     'nrpe_min': cmd.nrpe_min,
                     'nrpe_max': cmd.nrpe_max,
                     'nrpe_graphpoint': cmd.nrpe_graphpoint
                     }
        except:
            log.warn('Unable to pull previous NRPE Components')

        if "linux" in dmd_device_os:
            device_os = "linux"
        elif "windows" in dmd_device_os:
            device_os = "windows"
        else:
            device_os = "unknown"
            log.warn('Unable to determine OS. Skipping...')

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
            om.nrpe_min = results[cmd_index]['nrpe_min']
            om.nrpe_max = results[cmd_index]['nrpe_max']
            om.nrpe_graphpoint = results[cmd_index]['nrpe_graphpoint']

            rm.append(om)
        return rm
