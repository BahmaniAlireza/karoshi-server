#!/bin/bash
#Copyright (C) 2017  Paul Sharrad

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
############################
#Language
############################

STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/"$REMOTE_USER" ] && source /opt/karoshi/web_controls/user_prefs/"$REMOTE_USER"
export TEXTDOMAIN=karoshi-server

#Check if timout should be disabled
if [[ $(echo "$REMOTE_ADDR" | grep -c "$NOTIMEOUT") = 1 ]]
then
	TIMEOUT=86400
fi
############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '
<!DOCTYPE html>
<html>
<head>
  <title>'$"Setup Savapage"'</title><meta http-equiv="REFRESH" content="'"$TIMEOUT"'; URL=/cgi-bin/admin/logout.cgi">
<link rel="stylesheet" href="/css/'"$STYLESHEET"'?d='"$VERSION"'">
<script src="/all/stuHover.js" type="text/javascript"></script>
</head>
<body onLoad="start()"><div id="pagecontainer">'
#########################
#Get data input
#########################
DATA=$(cat | tr -cd 'A-Za-z0-9\._:%\-+')
#########################
#Assign data to variables
#########################
END_POINT=5
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

#Assign SERVERNAME
DATANAME=SERVERNAME
get_data
SERVERNAME="$DATAENTRY"

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'"$MESSAGE"'")';
echo 'window.location = "/cgi-bin/admin/karoshi_servers_view.cgi"'
echo '</script>'
echo "</div></body></html>"
exit
}

#########################
#Check data
#########################
#Check to see that servername is not blank
if [ -z "$SERVERNAME" ]
then
	MESSAGE=$"The servername cannot be blank."
	show_status
fi

#Check to see if this module has already been installed on the server
if [ -f /opt/karoshi/server_network/servers/"$SERVERNAME"/savapage ]
then
	STATUSMSG=$"This module has already been set up on this server."
fi

#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin

echo '
<form action="/cgi-bin/admin/module_savapage.cgi" method="post">
<div id="actionbox3"><div id="titlebox">

<table class="standard" style="text-align: left;" ><tr><td style="vertical-align: top;"><div class="sectiontitle">'$"Setup Savapage"' - '"$SERVERNAME"'</div></td><td style="vertical-align: top;">
<a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Print_Server"><img class="images" alt="" src="/images/help/info.png"><span>'$"This will set up the Savapage Libre Print Management System allowing Web Printing from all devices."' '$"Java and Libre Office will automatically be installed as part of this setup."'</span></a>
</td></tr></tbody></table><br></div><div id="infobox">

<input name="_SERVERNAME_" value="'"$SERVERNAME"'" type="hidden">
<b>'$"Description"'</b><br><br>
'$"This will set up the Savapage Libre Print Management System allowing Web Printing from all devices."'<br><br>More information can be found for Savapage at <a href="https://www.savapage.org/">www.savapage.org</a><br><br>'$"Java and Libre Office will automatically be installed as part of this setup."'<br><br>'"$STATUSMSG"'
<br><br>
<input value="'$"Submit"'" class="button" type="submit">
</div></div></form></div></body></html>'
exit
