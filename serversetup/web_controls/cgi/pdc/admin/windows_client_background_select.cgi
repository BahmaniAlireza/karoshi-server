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
#  _PRIGROUP_  primary group of the users to copy the profile to
############################
#Language
############################

STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
TEXTDOMAIN=karoshi-server

############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$"Windows Background - Select"'</title><meta http-equiv="REFRESH" content="0; URL=/cgi-bin/admin/windows_client_background_upload_fm.cgi"><link rel="stylesheet" href="/css/$STYLESHEET"><script src="/all/stuHover.js" type="text/javascript"></script></head><body><div id="pagecontainer">'
#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:\-'`
#########################
#Assign data to variables
#########################
DATA_ARRAY=( `echo $DATA | sed 's/_FILENAME_/_FILENAME_ /g' | sed 's/_PRIGROUP_/_PRIGROUP_ /g'` )
END_POINT=`echo ${#DATA_ARRAY[@]}`
let END_POINT=$END_POINT*2
#Assign PRIGROUP
COUNTER=2
ARRAY_COUNT=0
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = PRIGROUPcheck ]
then
let COUNTER=$COUNTER+1
PRIGROUP[$ARRAY_COUNT]=`echo $DATA | cut -s -d'_' -f$COUNTER`
let ARRAY_COUNT=$ARRAY_COUNT+1
fi
let COUNTER=$COUNTER+1
done
#Assign FILENAME
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = FILENAMEcheck ]
then
let COUNTER=$COUNTER+1
FILENAME=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
echo '</script>'
echo "</div></body></html>"
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
#Check to see that prigroup is not blank
if [ $PRIGROUP'null' = null ]
then
MESSAGE=$"You have not selected any groups."
show_status
fi
#Check to see that FILENAME is not blank
if [ $FILENAME'null' = null ]
then
MESSAGE=$"The filename cannot be blank."
show_status
fi
#Check that filename is a .bmp
if [ `echo $FILENAME | grep -c '\<bmp\>'` != 1 ]
then
MESSAGE=$"You have not uploaded a bmp file."
show_status
fi
#Check that background with this filename exists
if [ ! -f /var/www/karoshi/win_background_upload/$FILENAME ]
then
MESSAGE=$"You have not uploaded a bmp file."
show_status
fi
Checksum=`sha256sum /var/www/cgi-bin_karoshi/admin/windows_client_background_select.cgi | cut -d' ' -f1`
#Copy profiles to groups
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin

echo "<div id="actionbox">"
sudo -H /opt/karoshi/web_controls/exec/windows_client_background_select $REMOTE_USER:$REMOTE_ADDR:$Checksum:$FILENAME:`echo ${PRIGROUP[@]:0} | sed 's/ /:/g'`
EXEC_STATUS=`echo $?`
if [ $EXEC_STATUS = 0 ]
then
MESSAGE=`echo $"The background has been copied to all of the chosen groups."`
else
MESSAGE=`echo $"There was a problem with this action." $"Please check the karoshi web administration logs for more details."`
fi
show_status
exit
