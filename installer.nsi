; Bad Suika Game Installer Script
!define APPNAME "Bad Suika Game"
!define COMPANYNAME "Your Name"
!define DESCRIPTION "A fun fruit-dropping puzzle game"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0
!define HELPURL "https://github.com/yourusername/bad-suika-game"
!define UPDATEURL "https://github.com/yourusername/bad-suika-game"
!define ABOUTURL "https://github.com/yourusername/bad-suika-game"
!define INSTALLSIZE 50000

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\${APPNAME}"
Name "${APPNAME}"
Icon "watermelon.ico"
outFile "BadSuikaGameInstaller.exe"

!include LogicLib.nsh

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin"
    messageBox mb_iconstop "Administrator rights required!"
    setErrorLevel 740
    quit
${EndIf}
!macroend

function .onInit
    !insertmacro VerifyUserIsAdmin
functionEnd

page directory
page instfiles

section "install"
    setOutPath $INSTDIR
    
    ; File commands with proper error handling
    ; The file command uses relative paths from where makensis is run
    File "dist\Bad Suika Game.exe"
    
    ; Optional files (won't cause errors if missing)
    IfFileExists "watermelon.ico" 0 +2
    File "watermelon.ico"
    
    IfFileExists "README.txt" 0 +2
    File "README.txt"
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
    
    ; Create shortcuts
    CreateDirectory "$SMPROGRAMS\${APPNAME}"
    CreateShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\Bad Suika Game.exe" "" "$INSTDIR\watermelon.ico"
    CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\Bad Suika Game.exe" "" "$INSTDIR\watermelon.ico"
    
    ; Registry entries for Add/Remove Programs
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "InstallLocation" "$\"$INSTDIR$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayIcon" "$\"$INSTDIR\watermelon.ico$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "${COMPANYNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "HelpLink" "${HELPURL}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "URLUpdateInfo" "${UPDATEURL}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "URLInfoAbout" "${ABOUTURL}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMinor" ${VERSIONMINOR}
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoRepair" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "EstimatedSize" ${INSTALLSIZE}
    
    MessageBox MB_OK "Installation complete! Bad Suika Game has been installed."
sectionEnd

section "uninstall"
    Delete "$INSTDIR\Bad Suika Game.exe"
    Delete "$INSTDIR\watermelon.ico"
    Delete "$INSTDIR\README.txt"
    Delete "$INSTDIR\uninstall.exe"
    
    Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
    RMDir "$SMPROGRAMS\${APPNAME}"
    Delete "$DESKTOP\${APPNAME}.lnk"
    
    RMDir "$INSTDIR"
    
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
    
    MessageBox MB_OK "Uninstallation complete!"
sectionEnd