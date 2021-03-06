#!/bin/bash
#Copyright (C) 2010  Paul Sharrad
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#The Karoshi Team can be contacted at: 
#mpsharrad@karoshi.org.uk
#jsharrad@karoshi.org.uk

#
#Website: http://www.karoshi.org.uk

#Detect mobile browser
MOBILE=no
source /opt/karoshi/web_controls/detect_mobile_browser
source /opt/karoshi/web_controls/version


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
echo '<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="stylesheet" href="/css/'$STYLESHEET'?d='$VERSION'"><title>'$"Technical Support"'</title><meta name="viewport" content="width=device-width, initial-scale=1"> <!--480-->'
if [ $MOBILE = yes ]
then
echo '<link rel="stylesheet" type="text/css" href="/all/mobile_menu/sdmenu.css">
	<script src="/all/mobile_menu/sdmenu.js">
		/***********************************************
		* Slashdot Menu script- By DimX
		* Submitted to Dynamic Drive DHTML code library: www.dynamicdrive.com
		* Visit Dynamic Drive at www.dynamicdrive.com for full source code
		***********************************************/
	</script>
	<script>
	// <![CDATA[
	var myMenu;
	window.onload = function() {
		myMenu = new SDMenu("my_menu");
		myMenu.init();
	};
	// ]]>
	</script>'
fi
echo '</head><body><div id="pagecontainer">'
#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\.%+_:\-'`
#########################
#Assign data to variables
#########################
END_POINT=5
#Assign JOBNAME
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = JOBNAMEcheck ]
then
let COUNTER=$COUNTER+1
JOBNAME=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
echo 'window.location = "/cgi-bin/admin/helpdesk_view_fm.cgi";'
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
#Check data
#########################
#Check to see that JOBNAME is not blank
if [ $JOBNAME'null' = null ]
then
MESSAGE=$"The job name cannot be blank."
show_status
fi

if [ ! -f /opt/karoshi/server_network/helpdesk/todo/$JOBNAME ]
then
MESSAGE=$"This job does not exist."
show_status
fi

#Generate navigation bar
if [ $MOBILE = no ]
then
DIV_ID=actionbox
TABLECLASS=standard
WIDTH1=180
WIDTH2=200
WIDTH3=600
COLS=70
ROWS=6
/opt/karoshi/web_controls/generate_navbar_admin
else
DIV_ID=actionbox
TABLECLASS=mobilestandard
WIDTH1=120
WIDTH2=140
WIDTH3=140
COLS=18
ROWS=4
fi

echo '<form action="/cgi-bin/admin/helpdesk_action.cgi" method="post">'

[ $MOBILE = no ] && echo '<div id="'$DIV_ID'">'

#Show back button for mobiles
if [ $MOBILE = yes ]
then
echo '<div style="float: center" id="my_menu" class="sdmenu">
	<div class="expanded">
	<span>'$"Technical Support"' - '$"Action Request"'</span>
<a href="/cgi-bin/admin/mobile_menu.cgi">'$"Helpdesk"'</a>
</div></div><div id="mobileactionbox">'
else
echo '<b>'$"Technical Support"' - '$"Action Request"'</b><br><br>'
fi



#Get data
source /opt/karoshi/server_network/helpdesk/todo/$JOBNAME
source /opt/karoshi/web_controls/version

#Show job data

echo '<input name="_JOBNAME_" value="'$JOBNAME'" type="hidden">
<input name="_PRIORITY_" value="'$PRIORITY'" type="hidden">
<input name="_ASSIGNED_" value="'$ASSIGNED'" type="hidden">
<table class="'$TABLECLASS'" style="text-align: left;" >
<tbody>
<tr><td style="width: '$WIDTH1'px;">'$"Request Summary"'</td><td>'$JOBTITLE'</td></tr>
<tr><td>'$"Name"'</td><td>'$NAME'</td></tr>
<tr><td>'$"Location"'</td><td>'$LOCATION'</td></tr>
<tr><td>'$"Department"'</td><td>'$DEPARTMENT'</td></tr>
<tr><td>'$"Category"'</td><td>'$CATEGORY'</td></tr>
<tr><td>'$"Extended Details"'</td><td>'$REQUEST'</td></tr>
<tr><td>'$"Update"'</td><td><input tabindex= "1" name="_ACTION_"  checked="checked" value="update" type="radio"></td></tr>
<tr><td>'$"Completed"'</td><td><input tabindex= "3" name="_ACTION_" value="completed" type="radio"></td></tr>
<tr><td>'$"Feedback"'</td><td><textarea style="width: '$WIDTH3'px;" tabindex= "7" cols="'$COLS'" rows="'$ROWS'" name="_FEEDBACK_">'$FEEDBACK'</textarea></td></tr>
</tbody></table>'

if [ $MOBILE = no ]
then
echo '</div><div id="submitbox">'
fi

echo '<input value="'$"Submit"'" class="button" type="submit"> <input value="'$"Reset"'" class="button" type="reset">
</div></form></div></body></html>'
exit

