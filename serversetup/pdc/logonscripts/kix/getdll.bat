If not exist %LOGONSERVER%\applications\cups_print\pscript5.dll (
if exist C:\windows\"Driver Cache"\i386\driver.cab (
cd C:\windows\"Driver Cache"\i386\
expand driver.cab %LOGONSERVER%\applications\cups_print -F:pscript.hlp
)
if exist C:\windows\"Driver Cache"\i386\sp1.cab (
date /T > %LOGONSERVER%\applications\cups_print\dll_version.txt
echo DLLs obtained from: >> %LOGONSERVER%\applications\cups_print\dll_version.txt
echo Windows XP Service Pack 1 >> %LOGONSERVER%\applications\cups_print\dll_version.txt
cd C:\windows\"Driver Cache"\i386\
expand sp1.cab %LOGONSERVER%\applications\cups_print -F:pscript5.dll
expand sp1.cab %LOGONSERVER%\applications\cups_print -F:pscript.ntf
expand sp1.cab %LOGONSERVER%\applications\cups_print -F:ps5ui.dll
)
if exist C:\windows\"Driver Cache"\i386\sp2.cab (
date /T > %LOGONSERVER%\applications\cups_print\dll_version.txt
echo DLLs obtained from: >> %LOGONSERVER%\applications\cups_print\dll_version.txt
echo Windows XP Service Pack 2 >> %LOGONSERVER%\applications\cups_print\dll_version.txt
cd C:\windows\"Driver Cache"\i386\
expand sp2.cab %LOGONSERVER%\applications\cups_print -F:pscript5.dll
expand sp2.cab %LOGONSERVER%\applications\cups_print -F:pscript.ntf
expand sp2.cab %LOGONSERVER%\applications\cups_print -F:ps5ui.dll
)
if exist C:\winnt\"Driver Cache"\i386\sp4.cab (
date /T > %LOGONSERVER%\applications\cups_print\dll_version.txt
echo DLLs obtained from: >> %LOGONSERVER%\applications\cups_print\dll_version.txt
echo Windows 2000 Service pack 4 >> %LOGONSERVER%\applications\cups_print\dll_version.txt
cd C:\winnt\"Driver Cache"\i386\
expand sp4.cab %LOGONSERVER%\applications\cups_print -F:pscript.hlp
expand sp4.cab %LOGONSERVER%\applications\cups_print -F:pscript5.dll
expand sp4.cab %LOGONSERVER%\applications\cups_print -F:pscript.ntf
expand sp4.cab %LOGONSERVER%\applications\cups_print -F:ps5ui.dll
)
)

If not exist %LOGONSERVER%\applications\cups_print\x64\pscript5.dll (
if exist C:\Windows\System32\spool\drivers\x64\PCC\ntprint.inf*.cab (
C:\Windows\System32\expand.exe -I C:\Windows\System32\spool\drivers\x64\PCC\ntprint.inf*.cab -F:PS5UI.DLL %LOGONSERVER%\applications\cups_print\x64
C:\Windows\System32\expand.exe -I C:\Windows\System32\spool\drivers\x64\PCC\ntprint.inf*.cab -F:PSCRIPT.HLP %LOGONSERVER%\applications\cups_print\x64
C:\Windows\System32\expand.exe -I C:\Windows\System32\spool\drivers\x64\PCC\ntprint.inf*.cab -F:PSCRIPT.NTF %LOGONSERVER%\applications\cups_print\x64
C:\Windows\System32\expand.exe -I C:\Windows\System32\spool\drivers\x64\PCC\ntprint.inf*.cab -F:PSCRIPT5.DLL %LOGONSERVER%\applications\cups_print\x64
)
)

