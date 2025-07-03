@echo off
echo Building Bad Suika Game Installer...
echo.

REM Create icon first
echo Converting watermelon.png to watermelon.ico...
python convert_icon.py

REM Build executable
echo Building executable...
pyinstaller bad_suika_game.spec

REM Verify the executable was created
if not exist "dist\Bad Suika Game.exe" (
    echo ERROR: PyInstaller failed to create the executable!
    echo Check the PyInstaller output above for errors.
    pause
    exit /b 1
)

echo Executable created successfully!
echo.

REM Create simple installer directory
if not exist "installer" mkdir installer
if not exist "installer\BadSuikaGame" mkdir installer\BadSuikaGame

REM Copy files for simple installer
echo Copying files for simple installer...
copy "dist\Bad Suika Game.exe" "installer\BadSuikaGame\"
copy "README.txt" "installer\BadSuikaGame\" 2>nul

REM Create simple batch installer
echo Creating simple installer...
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

REM Try to create NSIS installer
echo.
echo Creating NSIS installer...
where makensis >nul 2>&1
if %errorlevel% == 0 (
    echo NSIS found! Building professional installer...
    makensis installer.nsi
    if exist "BadSuikaGameInstaller.exe" (
        echo SUCCESS: Professional installer created - BadSuikaGameInstaller.exe
    ) else (
        echo FAILED: NSIS compilation failed
        echo Check that all files exist:
        if exist "dist\Bad Suika Game.exe" (
            echo   ✓ dist\Bad Suika Game.exe found
        ) else (
            echo   ✗ dist\Bad Suika Game.exe NOT found
        )
        if exist "watermelon.ico" (
            echo   ✓ watermelon.ico found
        ) else (
            echo   ✗ watermelon.ico NOT found
        )
    )
) else (
    echo NSIS not found. Install NSIS from https://nsis.sourceforge.io/
)

echo.
echo Build Summary:
echo ==============
if exist "installer\install.bat" echo ✓ Simple installer: installer\install.bat
if exist "BadSuikaGameInstaller.exe" echo ✓ Professional installer: BadSuikaGameInstaller.exe
echo.
pause