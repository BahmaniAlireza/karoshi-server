#!/bin/bash
#Copyright (C) 2009  Paul Sharrad

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

#Detect mobile browser
MOBILE=no
source /opt/karoshi/web_controls/detect_mobile_browser

############################
#Language
############################
LANGCHOICE=englishuk
STYLESHEET=defaultstyle.css
TIMEOUT=300
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/system/dns ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/system/dns
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/all ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/all
############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$TITLE2'</title><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi">'
echo '<link rel="stylesheet" href="/css/'$STYLESHEET'"><script src="/all/stuHover.js" type="text/javascript"></script><meta name="viewport" content="width=device-width, initial-scale=1"> <!--480-->'

if [ $MOBILE = yes ]
then
echo '<link rel="stylesheet" type="text/css" href="/all/mobile_menu/sdmenu.css">
	<script type="text/javascript" src="/all/mobile_menu/sdmenu.js">
		/***********************************************
		* Slashdot Menu script- By DimX
		* Submitted to Dynamic Drive DHTML code library: http://www.dynamicdrive.com
		* Visit Dynamic Drive at http://www.dynamicdrive.com/ for full source code
		***********************************************/
	</script>
	<script type="text/javascript">
	// <![CDATA[
	var myMenu;
	window.onload = function() {
		myMenu = new SDMenu("my_menu");
		myMenu.init();
	};
	// ]]>
	</script>'
fi

echo '</head><body onLoad="start()">'

#Generate navigation bar
if [ $MOBILE = no ]
then
DIV_ID=actionbox
TABLECLASS=standard
WIDTH=180
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
else
DIV_ID=actionbox2
TABLECLASS=mobilestandard
fi

echo '<form action="/cgi-bin/admin/dnsview.cgi" method="post">'

[ $MOBILE = no ] && echo '<div id="'$DIV_ID'">'

#Show back button for mobiles
if [ $MOBILE = yes ]
then
echo '<div style="float: center" id="my_menu" class="sdmenu">
	<div class="expanded">
	<span>'$TITLE2'</span>
<a href="/cgi-bin/admin/mobile_menu.cgi">'$SYSMENUMSG'</a>
</div></div><div id="mobileactionbox">
'
else
echo '<b>'$TITLE2'</b> <a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=DNS"><img class="images" alt="" src="/images/help/info.png"><span>'$HELPMSG2'</span></a>
<br><br>'
fi

#Show main server
if [ $MOBILE = no ]
then
SERVERICON="/images/submenus/system/computer.png"
SERVERICON2="/images/submenus/system/all_computers.png"
else
SERVERICON="/images/submenus/system/computerm.png"
SERVERICON2="/images/submenus/system/all_computersm.png"
fi
if [ -f /opt/karoshi/server_network/info ]
then
source /opt/karoshi/server_network/info
LOCATION_NAME="- $LOCATION_NAME"
fi

WIDTH=90
[ $MOBILE = yes ] && WIDTH=70

echo '<b>'$MYSERVERSMSG' '$LOCATION_NAME'</b><table class="'$TABLECLASS'" style="text-align: left;" border="0" cellpadding="2" cellspacing="2"><tbody><tr>'

echo '<td style="width: '$WIDTH'px; vertical-align: top; text-align: left;"><a class="info" href="javascript:void(0)"><input name="_SERVERTYPE_network_SERVERNAME_'$HOSTNAME'_" type="image" class="images" src="'$SERVERICON'" value=""><span>'$HOSTNAME'</span></a><br>'$HOSTNAME'</td></tr>'

echo '</tbody></table><br>'

#Show list of federated servers
if [ -d /opt/karoshi/server_network/federated_ldap_servers/ ]
then
if [ `ls -1 /opt/karoshi/server_network/federated_ldap_servers/ | wc -l` -gt 0 ]
then
for FEDERATED_SERVERS in /opt/karoshi/server_network/federated_ldap_servers/*
do
FEDERATED_SERVER=`basename $FEDERATED_SERVERS`
if [ -f /opt/karoshi/server_network/federated_ldap_servers/$FEDERATED_SERVER/info ]
then
source /opt/karoshi/server_network/federated_ldap_servers/$FEDERATED_SERVER/info
LOCATION_NAME="- $LOCATION_NAME"
fi
echo '<b>'$FEDERATEDSERVERSMSG' '$LOCATION_NAME'</b><table class="'$TABLECLASS'" style="text-align: left;" border="0" cellpadding="2" cellspacing="2"><tbody><tr>'
echo '<td style="width: '$WIDTH'px; vertical-align: top; text-align: left;"><a class="info" href="javascript:void(0)"><input name="_SERVERTYPE_federated_SERVERNAME_'$FEDERATED_SERVER'_" type="image" class="images" src="'$SERVERICON'" value=""><span>'$FEDERATED_SERVER'</span></a><br>'$FEDERATED_SERVER'</td>'
echo '</tr></tbody></table><br>'
done
fi
fi

echo '</div></form></body></html>'
exit

