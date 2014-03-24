from Products.DataCollector.plugins.CollectorPlugin import (CollectorPlugin, SnmpPlugin, PythonPlugin)
from Products.DataCollector.DeviceProxy import DeviceProxy
import subprocess
import os

class Check_NRPE(PythonPlugin):
    relname = 'nrpeComponents'
    modname = 'ZenPacks.Secure24.Check_NRPE.nrpeComponent'

    # Define default check_nrpe checks used by Secure-24
    # These checks will be added to the device.
    def collect(self, device, log):
        nrpeCmdTableMaps = {}
        nrpeCmdTableMaps[0] = {
            'os': "windows",
            'title': 'Physical Memory Usage',
            'nrpe_cmd': 'CheckMem',
            'nrpe_args': 'ShowAll type=physical',
            'nrpe_timeout': 30,
            'nrpe_cycle': 5,
            'nrpe_retries': 3
            }

        nrpeCmdTableMaps[1] = {
            'os': "windows",
            'title': 'CPU Usage',
            'nrpe_cmd': 'CheckCPU',
            'nrpe_args': 'time=15m time=5m time=1m ShowAll',
            'nrpe_timeout': 30,
            'nrpe_cycle': 5,
            'nrpe_retries': 3
            }

        nrpeCmdTableMaps[2] = {
            'os': "linux",
            'title': 'DNS Lookups',
            'nrpe_cmd': 'check_dns_lookups',
            'nrpe_args': '""',
            'nrpe_timeout': 30,
            'nrpe_cycle': 5,
            'nrpe_retries': 3
            }

        nrpeCmdTableMaps[3] = {
            'os': "linux",
            'title': 'Read Only Mounts',
            'nrpe_cmd': 'nrpe-check_ro-mounts',
            'nrpe_args': None,
            'nrpe_timeout': 30,
            'nrpe_cycle': 5,
            'nrpe_retries': 3
            }

        nrpeCmdTableMaps[4] = {
            'os': "linux",
            'title': 'LDAP Connectivity',
            'nrpe_cmd': 'check_ldap_lookups',
            'nrpe_args': None,
            'nrpe_timeout': 30,
            'nrpe_cycle': 5,
            'nrpe_retries': 3
            }

        nrpeCmdTableMaps[5] = {
            'os': "linux",
            'title': 'NTP Offset',
            'nrpe_cmd': 'check_ntp_offset',
            'nrpe_args': None,
            'nrpe_timeout': 30,
            'nrpe_cycle': 5,
            'nrpe_retries': 3
            }

        # Add debug and error capturing
        host = "-H%s" % device.manageIp
        nrpe_cmd_line = os.environ['ZENHOME'] + '/libexec/plugins/check_nrpe'
        nrpe_proc = subprocess.Popen([nrpe_cmd_line, host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        nrpe_out, err = nrpe_proc.communicate()

        if "NRPE" in nrpe_out:
            device_os = "linux"
        elif "fine" in nrpe_out:
            device_os = "windows"
        else:
            device_os = "unknown"
            log.warn('Unable to determine OS. Skipping...')

        i = 0
        data = {}
        for cmd_index in nrpeCmdTableMaps:
            if nrpeCmdTableMaps[cmd_index]['os'] is not device_os:
                continue
            else:
                data[i] = nrpeCmdTableMaps[cmd_index]
                i += 1

        return data


    def process(self, device, results, log):
        rm = self.relMap()
        for cmd_index in results:
            om = self.objectMap()
            om.id = results[cmd_index]['title']
            om.title = results[cmd_index]['title']
            om.nrpe_cmd = results[cmd_index]['nrpe_cmd']
            om.nrpe_args = results[cmd_index]['nrpe_args']
            om.nrpe_timeout = results[cmd_index]['nrpe_timeout']
            om.nrpe_cycle = results[cmd_index]['nrpe_cycle']
            om.nrpe_retries = results[cmd_index]['nrpe_retries']

            rm.append(om)
        return rm
