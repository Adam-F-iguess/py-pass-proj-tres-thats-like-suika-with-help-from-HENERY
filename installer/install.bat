@echo off
echo Installing Bad Suika Game...
echo.
if not exist "%USERPROFILE%\Desktop\BadSuikaGame" mkdir "%USERPROFILE%\Desktop\BadSuikaGame"
copy "Bad Suika Game.exe" "%USERPROFILE%\Desktop\BadSuikaGame\"
echo.
echo Creating desktop shortcut...
cscript CreateShortcut.vbs
del CreateShortcut.vbs
echo.
echo Installation complete!
echo Bad Suika Game has been installed to your Desktop.
pause
