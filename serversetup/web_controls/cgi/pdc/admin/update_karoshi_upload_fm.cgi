#!/bin/bash
#copy_files_upload
#Copyright (C) 2012  Paul Sharrad

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
<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <TITLE>'$"Upload Web Management Patch"'</TITLE><meta http-equiv="REFRESH" content="'"$TIMEOUT"'; URL=/cgi-bin/admin/logout.cgi">
<link rel="stylesheet" href="/css/'"$STYLESHEET"'?d='"$VERSION"'">
<script src="/all/stuHover.js" type="text/javascript"></script>
</HEAD>
<body onLoad="start()"><div id="pagecontainer">'
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin

echo ' <FORM ENCTYPE="multipart/form-data" action="/cgi-bin/admin/update_karoshi_upload.cgi" method="post"><div id="actionbox3"><div id="titlebox">
<table class="standard" style="text-align: left;" ><tbody>
<tr><td style="vertical-align: top;"><div class="sectiontitle">'$"Upload Web Management Patch"'</div></td><td><a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$"This will allow you to upload and apply a web management updates to your server. You will also need the signature file to verify that it is a legitamate update."'</span></a></td></tr></tbody></table>
<P>
'"$UPLOADMSG"'
<P>
<table class="standard">
	<tr>
		<td>
			'$"Patch file"':
		</td>
		<td>
			<INPUT TYPE="FILE" NAME="file-to-upload-01" SIZE="35">
		</td>
	</tr>
	<tr>
		<td>
			'$"Sign file"':
		</td>
		<td>
			<INPUT TYPE="FILE" NAME="file-to-upload-02" SIZE="35">
		</td>
	</tr>
</table>
<br><br>
<input value="'$"Submit"'" class="button" type="submit"> <input value="'$"Reset"'" class="button" type="reset">
</div></div>
</form>
</div>
</BODY>
</HTML>
'
exit
