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
############################
#Language
############################
LANGCHOICE=englishuk
STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/user/lockout_reset ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/user/lockout_reset
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
<script type="text/javascript" src="/all/js/jquery.js"></script>
<script type="text/javascript" src="/all/js/script.js"></script>
<script src="/all/stuHover.js" type="text/javascript"></script>
</head>
<body onLoad="start()">'
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin

echo '<form action="/cgi-bin/admin/lockout_reset.cgi" method="post"><div id="actionbox"><b>'$TITLE'</b><br><br><div id="suggestions"></div>
  <table class="standard" style="text-align: left;" border="0" cellpadding="2" cellspacing="2">
    <tbody>
      <tr>
        <td style="width: 180px;">
'$USERNAMEMSG'</td>
        <td><input tabindex= "1" style="width: 200px;" name="_USERNAME_" size="20" type="text" id="inputString" onkeyup="lookup(this.value);"></td><td>
<a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Reset_User_Lockout"><img class="images" alt="" src="/images/help/info.png"><span>'$HELPMSG1'</span></a>

      </td></tr>
    </tbody>
  </table>
</div>
<div id="submitbox">
<input value="'$SUBMITMSG'" class="button" type="submit"> <input value="'$RESETMSG'" class="button" type="reset">
</div>
</form>
</body>
</html>
'
exit
