#!/bin/bash
#Copyright (C) 2007  Paul Sharrad

#This file is part of Karoshi Server.
#
#Karoshi Server is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Karoshi Server is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with Karoshi Server.  If not, see <http://www.gnu.org/licenses/>.

#
#The Karoshi Team can be contacted at: 
#mpsharrad@karoshi.org.uk
#jsharrad@karoshi.org.uk

#
#Website: http://www.karoshi.org.uk
########################
#Required input variables
########################
#  _FIRSTNAME_
#  _SURNAME_
# _USERNAMESTYLE_
#  _PASSWORD1_  Password used for new user
#  _PASSWORD2_  Checked against PASSWORD1 for typos.
#  _GROUP_      This is the primary group for the new user eg yr2000, staff, officestaff.
##########################
#Language
##########################

STYLESHEET=defaultstyle.css
[ -f "/opt/karoshi/web_controls/user_prefs/$REMOTE_USER" ] && source "/opt/karoshi/web_controls/user_prefs/$REMOTE_USER"
export TEXTDOMAIN=karoshi-server

##########################
#Show page
##########################
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$"Configure DHCP"'</title><link rel="stylesheet" href="/css/'"$STYLESHEET"'?d='"$VERSION"'"></head><body><div id="pagecontainer">'
#########################
#Get data input
#########################
DATA=$(cat | tr -cd 'A-Za-z0-9\._:%\+\-')
#########################
#Assign data to variables
#########################
END_POINT=30
function get_data {
COUNTER=2
DATAENTRY=""
while [[ $COUNTER -le $END_POINT ]]
do
	DATAHEADER=$(echo "$DATA" | cut -s -d'_' -f"$COUNTER")
	if [[ "$DATAHEADER" = "$DATANAME" ]]
	then
		let COUNTER="$COUNTER"+1
		DATAENTRY=$(echo "$DATA" | cut -s -d'_' -f"$COUNTER")
		break
	fi
	let COUNTER=$COUNTER+1
done
}

#Assign _DOMAINNAMESERVER_
DATANAME=DOMAINNAMESERVER
get_data
DOMAINNAMESERVER="$DATAENTRY"

#Assign _NETBIOSSERVER_
DATANAME=NETBIOSSERVER
get_data
NETBIOSSERVER="$DATAENTRY"

#Assign _ROUTER_
DATANAME=ROUTER
get_data
ROUTER=$(echo "$DATAENTRY" | tr -cd '0-9.')

#Assign _SUBNET_
DATANAME=SUBNET
get_data
SUBNET=$(echo "$DATAENTRY" | tr -cd '0-9.')

#Assign _SUBNETMASK_
DATANAME=SUBNETMASK
get_data
SUBNETMASK=$(echo "$DATAENTRY" | tr -cd '0-9.')

#Assign _STARTADDRESS_
DATANAME=STARTADDRESS
get_data
STARTADDRESS=$(echo "$DATAENTRY" | tr -cd '0-9.')

#Assign _ENDADDRESS_
DATANAME=ENDADDRESS
get_data
ENDADDRESS=$(echo "$DATAENTRY" | tr -cd '0-9.')

#Assign _DEFAULTLEASETIME_
DATANAME=DEFAULTLEASETIME
get_data
DEFAULTLEASETIME=$(echo "$DATAENTRY" | tr -cd '0-9')

#Assign _MAXLEASETIME_
DATANAME=MAXLEASETIME
get_data
MAXLEASETIME=$(echo "$DATAENTRY" | tr -cd '0-9')

#Assign _SECONDARYSERVER_
DATANAME=SECONDARYSERVER
get_data
SECONDARYSERVER="$DATAENTRY"

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'"$MESSAGE"'")';
echo 'window.location = "/cgi-bin/admin/dhcp_fm.cgi";'
echo '</script>'
echo "</div></div></body></html>"
exit
}

function show_status2 {
echo '<SCRIPT language="Javascript">'
echo 'window.location = "/cgi-bin/admin/dhcp_fm.cgi";'
echo '</script>'
echo "</div></div></body></html>"
exit
}

function check_tcpip {
INPUTCHECK=pass
#Check dots
if [[ $(echo "$IPDATA" | sed 's/\./\n /g'  | sed /^$/d | wc -l) != 4 ]]
then
	INPUTCHECK=fail
fi
#Check that no number is greater than 255
HIGHESTNUMBER=$(echo "$IPDATA" | sed 's/\./\n /g'  | sed /^$/d | sort -g -r | sed -n 1,1p)
if [ "$HIGHESTNUMBER" -gt 255 ]
then
	INPUTCHECK=fail
fi
}

function check_address {
PDCIP=$(hostname -i | cut -d" " -f1)

#Get netmask
MASK=$(ip -o -f inet addr show | grep "$PDCIP" | awk '/scope global/ {print $4}' | cut -d"/" -f2)
ZONEINFO1=$(ipcalc -n "$PDCIP"/"$MASK" | grep ^Network | sed "s/ * / /g" | cut -d" " -f2)
ZONEINFO2=$(ipcalc -n "$ADDRESS"/"$MASK" | grep ^Network | sed "s/ * / /g" | cut -d" " -f2)

if [[ "$ZONEINFO1" != "$ZONEINFO2" ]]
then
	MESSAGE=$"The start address and the end address have to be in the same range as the server address."
	show_status
fi
}

#########################
#Check https access
#########################
if [ https_"$HTTPS" != https_on ]
then
	export MESSAGE=$"You must access this page via https."
	show_status
fi
#########################
#Check user accessing this script
#########################
if [ ! -f /opt/karoshi/web_controls/web_access_admin ] || [ -z "$REMOTE_USER" ]
then
	MESSAGE=$"You must be a Karoshi Management User to complete this action."
	show_status
fi

if [[ $(grep -c ^"$REMOTE_USER": /opt/karoshi/web_controls/web_access_admin) != 1 ]]
then
	MESSAGE=$"You must be a Karoshi Management User to complete this action."
	show_status
fi

#Make sure we have ifconfig in the path
PATH=/usr/local/bin:/usr/bin:/bin:/sbin:/bin

#########################
#Check data
#########################

#Check to see that DOMAINNAMESERVER is not blank
if [ -z "$DOMAINNAMESERVER" ]
then
	MESSAGE=$"DNS Server Error"
	show_status
fi

#Check to see that NETBIOSSERVER is not blank
if [ -z "$NETBIOSSERVER" ]
then
	MESSAGE=$"Net Bios Server Error"
	show_status
fi

#Check to see that ROUTER is not blank
if [ -z "$ROUTER" ]
then
	MESSAGE=$"Router Error"
	show_status
fi
IPDATA=$ROUTER
check_tcpip
if [ "$INPUTCHECK" = fail ]
then
	MESSAGE=$"Router Error"
	show_status
fi
#Check to see that SUBNET is not blank
if [ -z "$SUBNET" ]
then
	MESSAGE=$"Subnet Error"
	show_status
fi
IPDATA=$SUBNET
check_tcpip
if [ "$INPUTCHECK" = fail ]
then
	MESSAGE=$"Subnet Error"
	show_status
fi
#Check to see that SUBNETMASK is not blank
if [ -z "$SUBNETMASK" ]
then
	MESSAGE=$"Subnet Mask Error"
	show_status
fi
IPDATA="$SUBNETMASK"
check_tcpip
if [ "$INPUTCHECK" = fail ]
then
	MESSAGE=$"Subnet Mask Error"
	show_status
fi
#Check to see that STARTADDRESS is not blank
if [ -z "$STARTADDRESS" ]
then
	MESSAGE=$"Range Error"
	show_status
fi
IPDATA="$STARTADDRESS"
check_tcpip
if [ "$INPUTCHECK" = fail ]
then
	MESSAGE=$"Range Error"
	show_status
fi
#Check to see that ENDADDRESS is not blank
if [ -z "$ENDADDRESS" ]
then
	MESSAGE=$"Range Error"
	show_status
fi
IPDATA="$ENDADDRESS"
check_tcpip
if [ "$INPUTCHECK" = fail ]
then
	MESSAGE=$"Range Error"
	show_status
fi

#Check that the start address is in the same range as the server.
ADDRESS="$STARTADDRESS"
check_address

#Check that the end address is in the same range as the server.
ADDRESS="$ENDADDRESS"
check_address

#Check to see that DEFAULTLEASETIME is not blank
if [ -z "$DEFAULTLEASETIME" ]
then
	MESSAGE=$"Lease Time Error"
	show_status
fi

#Check to see that MAXLEASETIME is not blank
if [ -z "$MAXLEASETIME" ]
then
	MESSAGE=$"Lease Time Error"
	show_status
fi

if [ "$DEFAULTLEASETIME" -gt "$MAXLEASETIME" ]
then
	MESSAGE=$"The default lease time cannot be greater than the maximum lease time."
	show_status
fi

#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
echo '<div id="actionbox3"><div id="titlebox"><div class="sectiontitle">'$"Configure DHCP"'</div><br>'

Checksum=$(sha256sum /var/www/cgi-bin_karoshi/admin/dhcp.cgi | cut -d' ' -f1)
echo "$REMOTE_USER:$REMOTE_ADDR:$Checksum:$DOMAINNAMESERVER:$NETBIOSSERVER:$ROUTER:$SUBNET:$SUBNETMASK:$STARTADDRESS:$ENDADDRESS:$DEFAULTLEASETIME:$MAXLEASETIME:$SECONDARYSERVER:" | sudo -H /opt/karoshi/web_controls/exec/dhcp
echo '<ul><li>'$"The DHCP changes have been applied."'</li></ul>'
sleep 3
show_status2
exit

