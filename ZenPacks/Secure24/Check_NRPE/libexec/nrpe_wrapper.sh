#!/bin/bash

# Check_NRPE wrapper for Zenoss NRPE checks.
# This is to provide additional data point for command errors.
# Contact EnterpriseMonitoringTeam@Secure-24.com for support.
# Created: 2013-11-19
# Modified: 2014-03-27

out=0
check_path="/usr/lib64/nagios/plugins"
check_nrpe="$ZENHOME/libexec/plugins/check_nrpe"
usage="Does not apply now. Usage: $0 IP CmdArgs\n\n
        IP: IP or Hostname of device to be checked\n
        CmdArgs: check_nrpe -c arguments. (optional)\n\n
        Example:\n
        $0 192.168.1.2\n
        This will do a basic check_nrpe -H <ip>\n
        $0 192.168.1.2 \"CheckMem -a ShowAll type=physical\"\n
        This will perform a check_nrpe -H <ip> -c CheckMem -a ShowAll type=physical\n\n
        Contact EnterpriseMonitoringTeam@Secure-24.com with any questions.\n"

if [ ! $# -gt 0 ]; then
        echo -e "${RedF}Incorrect arguments specified.${Reset}"
        exit 1;
fi

# Check for nrpe arguments.
# If none, do a normal check_nrpe with no command arguement.
if [ $# -eq 1 ]; then
        nrpe_cmd=$($check_path/check_nrpe -H $1) &> /dev/null
elif [ $# -eq 2 ]; then
	nrpe_cmd=$($check_path/check_nrpe -H $1 -t $2) &> /dev/null
elif [ $# -eq 3 ]; then
        nrpe_cmd=$($check_path/check_nrpe -H $1 -t $2 -c $3) &> /dev/null
else
	if [ "$4" == "None" ]; then
	        nrpe_cmd=$($check_path/check_nrpe -H $1 -t $2 -c $3) &> /dev/null
	else
		nrpe_cmd=$($check_path/check_nrpe -H $1 -t $2 -c $3 -a $4) &> /dev/null
	fi

fi

out=$?

# If check_nrpe exited with an error, add additional error output.
if [ $out -ne 0 ]; then
        # If error is a timeout, set special error code.
        # If not, let last error code equal error.
        timeout=$(echo "$nrpe_cmd" | grep -i "timeout")
        if [ -n "$timeout" ]; then
                output=-4
        else
                output=$(echo "-"$out)
        fi
else
	output=$out
fi

datasource=$(echo "$nrpe_cmd" | grep -i '|')
if [ -n "$datasource" ]; then
	output=$(echo "$nrpe_cmd" | cut -d'|' -f2 | cut -d'=' -f2)
fi

echo "$nrpe_cmd""|OUTPUT=$output"
exit $out
