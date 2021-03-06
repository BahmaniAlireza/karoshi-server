#!/bin/bash
#Copyright (C) 2010  Paul Sharrad

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

##########################
#Language
##########################

STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
TEXTDOMAIN=karoshi-server

##########################
#Show page
##########################
echo "Content-type: text/html"
echo ""
echo '
<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>'$"Create ZFS Raid"'</title>
  <link rel="stylesheet" href="/css/'$STYLESHEET'?d='$VERSION'"></head><body><div id="pagecontainer">'
#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:%/+-' | sed 's/____/QUADUNDERSCORE/g' | sed 's/_/12345UNDERSCORE12345/g' | sed 's/QUADUNDERSCORE/_/g'`
#########################
#Assign data to variables
#########################
END_POINT=30
#Assign SERVERNAME
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
	DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
	if [ `echo $DATAHEADER'check'` = SERVERNAMEcheck ]
	then
		let COUNTER=$COUNTER+1
		SERVERNAME=`echo $DATA | cut -s -d'_' -f$COUNTER`
		break
	fi
	let COUNTER=$COUNTER+1
done
#Assign SERVERTYPE
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
	DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
	if [ `echo $DATAHEADER'check'` = SERVERTYPEcheck ]
	then
		let COUNTER=$COUNTER+1
		SERVERTYPE=`echo $DATA | cut -s -d'_' -f$COUNTER`
		break
	fi
	let COUNTER=$COUNTER+1
done
#Assign SERVERMASTER
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
	DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
	if [ `echo $DATAHEADER'check'` = SERVERMASTERcheck ]
	then
		let COUNTER=$COUNTER+1
		SERVERMASTER=`echo $DATA | cut -s -d'_' -f$COUNTER`
		break
	fi
	let COUNTER=$COUNTER+1
done

#Assign ACTION
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
	DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
	if [ `echo $DATAHEADER'check'` = ACTIONcheck ]
	then
		let COUNTER=$COUNTER+1
		ACTION=`echo $DATA | cut -s -d'_' -f$COUNTER`
		break
	fi
	let COUNTER=$COUNTER+1
done
#Assign DRIVES
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
	DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
	if [ `echo $DATAHEADER'check'` = DRIVEcheck ]
	then
		let COUNTER=$COUNTER+1
		DRIVE=`echo $DATA | cut -s -d'_' -f$COUNTER | sed 's/%2F/\//g' | sed 's/12345UNDERSCORE12345/_/g'`
		DRIVES=`echo $DRIVES,$DRIVE`
	fi
	let COUNTER=$COUNTER+1
done
DRIVES=`echo $DRIVES | sed 's/^,//g'`
#Assign PARITY
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
	DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
	if [ `echo $DATAHEADER'check'` = PARITYcheck ]
	then
		let COUNTER=$COUNTER+1
		PARITY=`echo $DATA | cut -s -d'_' -f$COUNTER | sed 's/12345UNDERSCORE12345/_/g'`
		break
	fi
	let COUNTER=$COUNTER+1
done

#Assign CREATETYPE
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
	DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
	if [ `echo $DATAHEADER'check'` = CREATETYPEcheck ]
	then
		let COUNTER=$COUNTER+1
		CREATETYPE=`echo $DATA | cut -s -d'_' -f$COUNTER | sed 's/12345UNDERSCORE12345/_/g'`
		break
	fi
	let COUNTER=$COUNTER+1
done

#Assign MOUNTPOINT
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
	DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
	if [ `echo $DATAHEADER'check'` = MOUNTPOINTcheck ]
	then
		let COUNTER=$COUNTER+1
		MOUNTPOINT=`echo $DATA | cut -s -d'_' -f$COUNTER | sed 's/%2F/\//g' | sed 's/%2F/\//g'`
		break
	fi
	let COUNTER=$COUNTER+1
done


function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'");'
echo '</script>
<form METHOD=POST ACTION="/cgi-bin/admin/zfs_raid_create.cgi" target="_top" name = "frm">
<input type="hidden" name="____SERVERNAME____" value="'$SERVERNAME'">
<input type="hidden" name="____SERVERTYPE____" value="'$SERVERTYPE'">
<input type="hidden" name="____SERVERMASTER____" value="'$SERVERMASTER'">
</form>
<script>
document.frm.submit();
</script>
'
echo "</div></div></body></html>"
exit
}

function control_raid {
echo '
<form METHOD=POST ACTION="/cgi-bin/admin/zfs_raid_control.cgi" target="_top" name = "frm">
<input type="hidden" name="____SERVERNAME____" value="'$SERVERNAME'">
<input type="hidden" name="____SERVERTYPE____" value="'$SERVERTYPE'">
<input type="hidden" name="____SERVERMASTER____" value="'$SERVERMASTER'">
</form>
<script>
document.frm.submit();
</script>
'
[ $MOBILE = no ] && echo '</div>'

echo "</div></div></body></html>"
exit
}
#########################
#Check https access
#########################
if [ https_$HTTPS != https_on ]
then
	export MESSAGE=$"You must access this page via https."
	show_status
fi
#########################
#Check user accessing this script
#########################
if [ ! -f /opt/karoshi/web_controls/web_access_admin ] || [ $REMOTE_USER'null' = null ]
then
	MESSAGE=$"You must be a Karoshi Management User to complete this action."
	show_status
fi

if [ `grep -c ^$REMOTE_USER: /opt/karoshi/web_controls/web_access_admin` != 1 ]
then
	MESSAGE=$"You must be a Karoshi Management User to complete this action."
	show_status
fi
#########################
#Check data
#########################

#Check to see that SERVERNAME is not blank
if [ -z "$SERVERNAME" ]
then
	MESSAGE=$"The server cannot be blank."
	show_status
fi

#Check to see that SERVERTYPE is not blank
if [ -z "$SERVERTYPE" ]
then
	MESSAGE=$"The servertype cannot be blank."
	show_status
fi

#Check to see that SERVERMASTER is not blank
if [ $SERVERTYPE = federatedslave ]
then
	if [ -z "$SERVERMASTER" ]
	then
		MESSAGE=$"The servermaster cannot be blank."
		show_status
	fi
fi

#Check to see that CREATETYPE is not blank
if [ -z "$CREATETYPE" ]
then
	MESSAGE=$"You have not selected a raid type."
	show_status
fi

if [ $CREATETYPE = create ]
then
	#Check to see that PARITY is not blank
	if [ -z "$PARITY" ]
	then
		MESSAGE="You have not chosen a parity level."
		show_status
	fi

	if [ -z "$DRIVES" ]
	then
		MESSAGE=$"No drives have been selected."
		show_status
	fi


	if [ -z "$PARITY" ]
	then
		MESSAGE="You have not chosen a create type."
		show_status
	fi

	#Check to see that MOUNTPOINT is not blank
	if [ -z "$MOUNTPOINT" ]
	then
		MESSAGE=$"The mount point cannot be blank."
		show_status
	fi


	#Check that MOUNTPOINT is in an allowed area
	if [ `echo $MOUNTPOINT | grep -c ^/home` = 0 ] && [ `echo $MOUNTPOINT | grep -c ^/media/` = 0 ] && [ `echo $MOUNTPOINT | grep -c ^/mnt/` = 0 ] && [ `echo $MOUNTPOINT | grep -c ^/var` = 0 ]
	then
		MESSAGE=$"The mount point does not contain an allowed path."
		show_status
	fi


	#Sort out drives and spare drives

	SPAREDRIVES=`echo -e $DRIVES | sed "s/,/\n/g" | grep spare`
	DRIVES=`echo -e $DRIVES | sed "s/,/\n/g" | grep use`

	SPAREDRIVES=`echo $SPAREDRIVES | sed "s/ /,/g" | sed "s/spare//g"`
	DRIVES=`echo $DRIVES | sed "s/ /,/g" | sed "s/use//g"`

	#Check that enough drives have been selected
	MINDRIVES=2
	[ $PARITY = 2 ] && MINDRIVES=3
	[ $PARITY = 3 ] && MINDRIVES=4

	if [ `echo $DRIVES | sed 's/,/\n/g' | wc -l` -lt $MINDRIVES ]
	then
		MESSAGE=$"You have not selected enough drives for this raid type."
		show_status
	fi
fi

MOBILE=no
source /opt/karoshi/web_controls/detect_mobile_browser
source /opt/karoshi/web_controls/version

#Generate navigation bar
if [ $MOBILE = no ]
then
DIV_ID=actionbox3
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
else
DIV_ID=menubox
fi

echo '<div id="'$DIV_ID'">'

[ $MOBILE = no ] && echo '<div id="titlebox">'

#Show back button for mobiles
if [ $MOBILE = yes ]
then
	echo '<table class="standard" style="text-align: left;">
<tbody><tr><td style="vertical-align: top;"><a href="/cgi-bin/admin/mobile_menu.cgi"><img border="0" src="/images/submenus/mobile/back.png" alt="'$"Back"MSG'"></a></td>
<td style="vertical-align: middle;"><a href="/cgi-bin/admin/mobile_menu.cgi"><b>'$"Create ZFS Raid" - $SERVER'</b></a></td></tr></tbody></table>'
else
	echo '<b>'$"Create ZFS Raid" - $SERVERNAME'</b><br><br>'
fi

[ $MOBILE = no ] && echo '</div><div id="infobox">'

Checksum=`sha256sum /var/www/cgi-bin_karoshi/admin/zfs_raid_create2.cgi | cut -d' ' -f1`
echo "$REMOTE_USER:$REMOTE_ADDR:$Checksum:$SERVERNAME:$SERVERTYPE:$SERVERMASTER:$ACTION:$PARITY:$DRIVES:$SPAREDRIVES:$MOUNTPOINT:$CREATETYPE" | sudo -H /opt/karoshi/web_controls/exec/zfs_raid_create2
control_raid
exit
