echo Set oWS = WScript.CreateObject("WScript.Shell") 
echo sLinkFile = "%USERPROFILE%\Desktop\Bad Suika Game.lnk" 
echo Set oLink = oWS.CreateShortcut(sLinkFile) 
echo oLink.TargetPath = "%USERPROFILE%\Desktop\BadSuikaGame\Bad Suika Game.exe" 
echo oLink.Save 
