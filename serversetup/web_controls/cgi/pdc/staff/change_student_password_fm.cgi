#!/bin/bash
#Copyright (C) 2007  Paul Sharrad
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
############################
#Language
############################

STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/global_prefs ] && source /opt/karoshi/web_controls/global_prefs

#Detect mobile browser
MOBILE=no
source /opt/karoshi/web_controls/detect_mobile_browser

############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>'$"Change a Student's Password"'</title>
  <link rel="stylesheet" href="/css/'$STYLESHEET'?d='`date +%F`'">
<script type="text/javascript" src="/all/js/jquery.js"></script>
<script type="text/javascript" src="/all/js/script.js"></script>
<META HTTP-EQUIV="refresh" CONTENT="300; URL=/cgi-bin/blank.cgi">
<script src="/all/stuHover.js" type="text/javascript"></script><meta name="viewport" content="width=device-width, initial-scale=1"> <!--480-->'
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

echo '</head><body><div id="pagecontainer">'


#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:%\-+-'`
#########################
#Assign data to variables
#########################
END_POINT=10

#Assign USERNAME
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = USERNAMEcheck ]
then
let COUNTER=$COUNTER+1
USERNAME=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done
#Assign PASSWORD1
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = PASSWORD1check ]
then
let COUNTER=$COUNTER+1
PASSWORD1=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done
#Assign PASSWORD2
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = PASSWORD2check ]
then
let COUNTER=$COUNTER+1
PASSWORD2=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done



#Generate navigation bar
if [ $MOBILE = no ]
then
DIV_ID=actionbox
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_staff
else
DIV_ID=mobileactionbox
fi

echo '<form action="/cgi-bin/staff/change_student_password.cgi" method="post">'

#Show back button for mobiles
if [ $MOBILE = yes ]
then
echo '<div style="float: center" id="my_menu" class="sdmenu">
	<div class="expanded">
	<span>'$"Change a Student's Password"'</span>
<a href="/cgi-bin/staff/mobile_menu.cgi">'$"User Menu"'</a>
</div></div>
'
else
echo '<div id="'$DIV_ID'"><b>'$"Change a Student's Password"'</b><br><br>'
fi

if [ $MOBILE = yes ]
then
echo '<div id="mobileactionbox"><div id="suggestions"></div>'$"Student Username"'<br>
<input tabindex= "3" name="_USERNAME_" AUTOCOMPLETE = "off" style="width: 200px;" value="'$USERNAME'" size="20" type="text" id="inputString" onkeyup="lookup(this.value);"><br>
'$"Student Password"'<br>
<input tabindex= "4" name="_PASSWORD1_" style="width: 200px;" value="'$PASSWORD1'" size="20" type="password"><br>
'$"Confirm Password"'<br>
<input tabindex= "5" name="_PASSWORD2_" style="width: 200px;" value="'$PASSWORD2'" size="20" type="password"><br>
'$"View User Image"'<br>
<a class="info" href="javascript:void(0)"><input name="_VIEWIMAGE_yes_" type="image" class="images" src="/images/submenus/user/user_photo.png" value=""><span>'$"View User Image"'</span></a><br><br>
'
else
echo '<table class="standard" style="text-align: left;" border="0" cellpadding="2" cellspacing="2">
	<tbody>
		<tr>
			<td style="width: 180px;">
				'$"Student Username"'
			</td>
			<td>
				<div id="suggestions"></div>
				<input tabindex= "3" name="_USERNAME_" AUTOCOMPLETE = "off" style="width: 200px;" value="'$USERNAME'" size="20" type="text" id="inputString" onkeyup="lookup(this.value);">
			</td>
			<td>
				<a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$"This will change the password of the user for access to all servers on the Karoshi system including moodle and email."'</span></a>
			</td>
			<td colspan="1" rowspan="4" style="vertical-align: top;">
				<div id="photobox"><img src="/images/blank_user_image.jpg" width="140" height="180"></div>
			</td>
		</tr>
		<tr>
			<td>
				'$"Student Password"'
			</td>
			<td>
				<input tabindex= "4" name="_PASSWORD1_" style="width: 200px;" value="'$PASSWORD1'" size="20" type="password">
			</td>
			<td><a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$"Enter in the new password that you want the user to have."'<br><br>'$"The following special characters are allowed"':<br><br>space ! # $ & ( ) + - =  %</span></a>
			</td>
		</tr>
		<tr>
			<td>
				'$"Confirm Password"'
			</td>
			<td>
				<input tabindex= "5" name="_PASSWORD2_" style="width: 200px;" value="'$PASSWORD2'" size="20" type="password">
			</td>
		</tr>
		<tr>
			<td>
				'$"View User Image"'
			</td>
			<td>
				<a class="info" href="javascript:void(0)"><input name="_VIEWIMAGE_yes_" type="image" class="images" src="/images/submenus/user/user_photo.png" value=""><span>'$"View User Image"'</span></a>
			</td>
      		</tr>
	</tbody>
  </table>'
fi

#Get user image
if [ $USERNAME'blank' != blank ]
then
echo '<br>'
echo "$REMOTE_USER:$REMOTE_ADDR:$MD5SUM:$USERNAME:" | sudo -H /opt/karoshi/web_controls/exec/show_user_image
fi


if [ $MOBILE = no ]
then
echo '</div><div id="submitbox">'
else
echo '<br>'
fi
echo '<input value="'$"Submit"'" class="button" type="submit"> <input value="'$"Reset"'" class="button" type="reset"></div></form></div></body></html>'
exit

########################
#Unique key
########################
#mLh65dMUNZnij-A2A5deQLiCd
