@echo off
echo Building Bad Suika Game Installer...
echo.

REM Create icon
echo Converting watermelon.png to watermelon.ico...
python convert_icon.py

REM Build executable
echo Building executable...
pyinstaller bad_suika_game.spec

REM Create installer directory
if not exist "installer" mkdir installer
if not exist "installer\BadSuikaGame" mkdir installer\BadSuikaGame

REM Copy files
echo Copying files...
copy "dist\Bad Suika Game.exe" "installer\BadSuikaGame\"
copy "README.txt" "installer\BadSuikaGame\" 2>nul

REM Create installer batch file
echo Creating installer...
(
echo @echo off
echo echo Installing Bad Suika Game...
echo echo.
echo if not exist "%%USERPROFILE%%\Desktop\BadSuikaGame" mkdir "%%USERPROFILE%%\Desktop\BadSuikaGame"
echo copy "Bad Suika Game.exe" "%%USERPROFILE%%\Desktop\BadSuikaGame\"
echo echo.
echo echo Creating desktop shortcut...
echo echo Set oWS = WScript.CreateObject("WScript.Shell"^) > CreateShortcut.vbs
echo echo sLinkFile = "%%USERPROFILE%%\Desktop\Bad Suika Game.lnk" >> CreateShortcut.vbs
echo echo Set oLink = oWS.CreateShortcut(sLinkFile^) >> CreateShortcut.vbs
echo echo oLink.TargetPath = "%%USERPROFILE%%\Desktop\BadSuikaGame\Bad Suika Game.exe" >> CreateShortcut.vbs
echo echo oLink.Save >> CreateShortcut.vbs
echo cscript CreateShortcut.vbs
echo del CreateShortcut.vbs
echo echo.
echo echo Installation complete!
echo echo Bad Suika Game has been installed to your Desktop.
echo pause
) > "installer\install.bat"

echo.
echo Build complete! Check the 'installer' folder.
pause