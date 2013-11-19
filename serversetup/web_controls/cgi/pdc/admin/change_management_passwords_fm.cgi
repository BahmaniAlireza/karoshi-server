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
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/system/change_management_passwords ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/system/change_management_passwords
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/all ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/all
#Check if timout should be disabled
if [ `echo $REMOTE_ADDR | grep -c $NOTIMEOUT` = 1 ]
then
TIMEOUT=86400
fi
############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>'$TITLE'</title><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi">
<link rel="stylesheet" href="/css/'$STYLESHEET'">
<script src="/all/stuHover.js" type="text/javascript"></script>
</head>
<body onLoad="start()">'

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
WIDTH=160
fi

echo '<form action="/cgi-bin/admin/change_management_passwords.cgi" method="post"><div id="actionbox"><span style="font-weight: bold;">'$TITLE'</span> <a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Management_Passwords"><img class="images" alt="" src="/images/help/info.png"><span>'$HELPMSG6'</span></a>
<br><br>
<table class="standard" style="text-align: left;" border="0" cellpadding="2" cellspacing="2"><tbody>
<tr><td style="width: 180px;">System Password</td><td>
<select name="____USERACCOUNT____"  tabindex="1" style="width: 200px;">
<option></option>
<option>karoshi</option>
<option>Administrator</option>
<option>mysql</option>
'
#<option value="sambaroot">Samba Root</option>
echo '<option>root</option>
</select></td><td><a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Management_Passwords"><img class="images" alt="" src="/images/help/info.png"><span><b>Karoshi</b> - '$HELPMSG1'<br><br><b>Sambaroot</b> - '$HELPMSG2'<br><br><b>Root</b> - '$HELPMSG3'</span></a>
</td></tr>
<tr><td>'$NEWPASSMSG'</td><td><input name="____PASSWORD1____"  tabindex="2" size="20" style="width: 200px;" type="password"></td><td>
<a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Management_Passwords"><img class="images" alt="" src="/images/help/info.png"><span>'$PASSWORDHELP1'<br><br><b>'$SPECIALCHARSMSG'</b><br><br>'$CHARACTERHELP' space !	"	# 	$	%	& 	(	) 	*	+	, 	-	.	/ 	:
;	<	=	>	?	@ 	[	\	]	^	_	` 	{	|	}	~
</span></a>
</td></tr>
<tr><td>'$CONFIRMPASSMSG'</td><td><input name="____PASSWORD2____"  tabindex="3" size="20" style="width: 200px;" type="password"></td></tr>
</tbody></table><br><br>'

#Show list of ssh enabled servers
SERVERCOUNTER=0
SERVERLISTCOUNT=0
ROWCOUNT=6
[ $MOBILE = yes ] && ROWCOUNT=3
WIDTH=90
[ $MOBILE = yes ] && WIDTH=70
SERVERICON="/images/submenus/system/computer.png"
SERVERICON2="/images/submenus/system/all_computers.png"
if [ -f /opt/karoshi/server_network/info ]
then
source /opt/karoshi/server_network/info
LOCATION_NAME="- $LOCATION_NAME"
fi
echo '<b>'$MYSERVERSMSG' '$LOCATION_NAME'</b><table class="'$TABLECLASS'" style="text-align: left;" border="0" cellpadding="2" cellspacing="2"><tbody><tr>'
for KAROSHI_SERVER in /opt/karoshi/server_network/servers/*
do
KAROSHISERVER=`basename $KAROSHI_SERVER`
[ $SERVERCOUNTER = $ROWCOUNT ] && echo '</tr><tr>'
echo '<td style="width: '$WIDTH'px; vertical-align: top; text-align: left;"><a class="info" href="javascript:void(0)"><input name="____SERVERTYPE____network____SERVERNAME____'$KAROSHISERVER'____" type="image" class="images" src="'$SERVERICON'" value=""><span>'$KAROSHISERVER'<br><br>'
cat /opt/karoshi/server_network/servers/$KAROSHISERVER/* | sed '/<a href/c'"&nbsp"
echo '</span></a><br>'$KAROSHISERVER'</td>'
let SERVERCOUNTER=$SERVERCOUNTER+1
[ $SERVERCOUNTER -gt $ROWCOUNT ] && SERVERCOUNTER=1
let SERVERLISTCOUNT=$SERVERLISTCOUNT+1
done
echo '</tr></tbody></table><br>'


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
echo '<td style="width: '$WIDTH'px; vertical-align: top; text-align: left;"><a class="info" href="javascript:void(0)"><input name="____SERVERTYPE____federated____SERVERNAME____'$FEDERATED_SERVER'____" type="image" class="images" src="'$SERVERICON'" value=""><span>'$FEDERATED_SERVER'<br><br>'
cat /opt/karoshi/server_network/federated_ldap_servers/$FEDERATED_SERVER/servers/$FEDERATED_SERVER/* | sed '/<a href/c'"&nbsp"
echo '</span></a><br>'$FEDERATED_SERVER'</td>'
let SERVERLISTCOUNT=$SERVERLISTCOUNT+1
SERVERCOUNTER2=1
for FEDERATED_SLAVE_SERVERS in /opt/karoshi/server_network/federated_ldap_servers/$FEDERATED_SERVER/servers/*
do
FEDERATED_SLAVE_SERVER=`basename $FEDERATED_SLAVE_SERVERS`
if [ $FEDERATED_SLAVE_SERVER != $FEDERATED_SERVER ]
then
[ $SERVERCOUNTER2 = $ROWCOUNT ] && echo '</tr><tr>'
echo '<td style="width: '$WIDTH'px; vertical-align: top; text-align: left;"><a class="info" href="javascript:void(0)"><input name="____SERVERTYPE____federatedslave____SERVERMASTER____'$FEDERATED_SERVER'____SERVERNAME____'$FEDERATED_SLAVE_SERVER'____" type="image" class="images" src="'$SERVERICON'" value=""><span>'$FEDERATED_SLAVE_SERVER'<br><br>'
cat /opt/karoshi/server_network/federated_ldap_servers/$FEDERATED_SERVER/servers/$FEDERATED_SLAVE_SERVER/* | sed '/<a href/c'"&nbsp"
echo '</span></a><br>'$FEDERATED_SLAVE_SERVER'</td>'
let SERVERCOUNTER2=$SERVERCOUNTER2+1
[ $SERVERCOUNTER2 -gt $ROWCOUNT ] && SERVERCOUNTER2=1
fi
done
echo '</tr></tbody></table><br>'
done
fi
fi


if [ $SERVERLISTCOUNT -gt 1 ] 
then
echo '<b>'$ALLSERVERSMSG'</b><table class="'$TABLECLASS'" style="text-align: left;" border="0" cellpadding="2" cellspacing="2"><tbody><tr><td style="width: '$WIDTH'px; vertical-align: top; text-align: left;"><a class="info" href="javascript:void(0)"><input name="_SERVERTYPE_network_SERVERNAME_allservers_" type="image" class="images" src="'$SERVERICON2'" value=""><span>'$ALLSERVERMSG'</span></a><br>'$ALLSERVERMSG'</td></tr></tbody></table>'
fi

echo '</div></form></body></html>'

exit

