#!/bin/bash
#Copyright (C) 2007 Paul Sharrad

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
#jharris@karoshi.org.uk
#aball@karoshi.org.uk
#
#Website: http://www.karoshi.org.uk
########################
#Required input variables
########################
#  _WEBADDRESS_
#  _FILTERGROUP_  staff and students
############################
#Language
############################
LANGCHOICE=englishuk
STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/internet/dg_part_banned_sites ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/internet/dg_part_banned_sites
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/all ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/all
############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$TITLE'</title><meta http-equiv="REFRESH" content="0; URL='$HTTP_REFERER'"><link rel="stylesheet" href="/css/'$STYLESHEET'?d='`date +%F`'"></head><body><div id="pagecontainer">'
#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:%/-'`
#########################
#Assign data to variables
#########################
END_POINT=6
#Assign WEBADDRESS
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = WEBADDRESScheck ]
then
let COUNTER=$COUNTER+1
WEBADDRESS=`echo $DATA | cut -s -d'_' -f$COUNTER | tr 'A-Z' 'a-z' | sed 's/^http%3a%2f%2f//g'`
WEBADDRESS=`echo $WEBADDRESS | sed 's/^www.//g' | sed 's/%2f/\//g'`
WEBADDRESS=`echo $WEBADDRESS | tr -cd 'A-Za-z0-9\._/-'`
break
fi
let COUNTER=$COUNTER+1
done
#Assign SERVER
COUNTER=2
ARRAY_COUNT=0
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = FILTERGROUPcheck ]
then
let COUNTER=$COUNTER+1
FILTERGROUP[$ARRAY_COUNT]=`echo $DATA | cut -s -d'_' -f$COUNTER`
let ARRAY_COUNT=$ARRAY_COUNT+1
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
export MESSAGE=$HTTPS_ERROR
show_status
fi
#########################
#Check user accessing this script
#########################
if [ ! -f /opt/karoshi/web_controls/web_access_admin ] || [ $REMOTE_USER'null' = null ]
then
MESSAGE=$ACCESS_ERROR1
show_status
fi

if [ `grep -c ^$REMOTE_USER: /opt/karoshi/web_controls/web_access_admin` != 1 ]
then
MESSAGE=$ACCESS_ERROR1
show_status
fi
#########################
#Check data
#########################
#Check to see that WEBADDRESS is not blank
if [ $WEBADDRESS'null' = null ]
then
MESSAGE=$ERRORMSG1
show_status
fi
#Check to see that FILTERGROUP is not blank
if [ $FILTERGROUP'null' = null ]
then
MESSAGE=$ERRORMSG2
show_status
fi

#Check to see that FILTERGROUP has correct data
if [ `echo ${FILTERGROUP[@]:0} | grep -c -w Students` != 1 ] && [ `echo ${FILTERGROUP[@]:0} | grep -c -w Staff` != 1 ]
then
MESSAGE=$ERRORMSG3
show_status
fi

MD5SUM=`md5sum /var/www/cgi-bin_karoshi/admin/dg_part_banned_sites.cgi | cut -d' ' -f1`
sudo -H /opt/karoshi/web_controls/exec/dg_part_banned_sites $REMOTE_USER:$REMOTE_ADDR:$MD5SUM:$WEBADDRESS:`echo ${FILTERGROUP[@]:0} | sed 's/ /:/g'`
MESSAGE=`echo $WEBADDRESS: ${FILTERGROUP[@]:0}: $COMPLETEDMSG`
show_status
