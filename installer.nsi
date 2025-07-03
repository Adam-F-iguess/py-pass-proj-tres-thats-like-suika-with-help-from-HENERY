; Bad Suika Game Installer Script
!define APPNAME "Bad Suika Game"
!define COMPANYNAME "Your Name"
!define DESCRIPTION "A fun fruit-dropping puzzle game"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0
!define HELPURL "https://github.com/Adam-F-iguess/py-pass-proj-tres-thats-like-suika-with-help-from-HENERY"
!define UPDATEURL "https://github.com/Adam-F-iguess/py-pass-proj-tres-thats-like-suika-with-help-from-HENERY"
!define ABOUTURL "https://github.com/Adam-F-iguess/py-pass-proj-tres-thats-like-suika-with-help-from-HENERY"
!define INSTALLSIZE 50000

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\${APPNAME}"
Name "${APPNAME}"
Icon "watermelon.ico"
outFile "BadSuikaGameInstaller.exe"

!include LogicLib.nsh
!include "MUI2.nsh"

; Variables for checkboxes
Var LaunchCheckbox
Var LaunchCheckboxHwnd
Var ReleaseNotesCheckbox
Var ReleaseNotesCheckboxHwnd

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

; Custom finish page function
Function FinishPage
    !insertmacro MUI_HEADER_TEXT "Installation Complete" "Choose your next steps"
    
    nsDialogs::Create 1018
    Pop $0
    
    ${If} $0 == error
        Abort
    ${EndIf}
    
    ; Create launch checkbox
    ${NSD_CreateCheckbox} 10 20 100% 12u "Launch Bad Suika Game now"
    Pop $LaunchCheckboxHwnd
    ${NSD_SetState} $LaunchCheckboxHwnd ${BST_CHECKED}
    
    ; Create release notes checkbox  
    ${NSD_CreateCheckbox} 10 40 100% 12u "View release notes on GitHub"
    Pop $ReleaseNotesCheckboxHwnd
    ${NSD_SetState} $ReleaseNotesCheckboxHwnd ${BST_UNCHECKED}
    
    ; Add some explanatory text
    ${NSD_CreateLabel} 10 70 100% 24u "Thank you for installing Bad Suika Game!$\r$\nEnjoy dropping fruits and making combinations!"
    Pop $0
    
    nsDialogs::Show
FunctionEnd

; Handle finish page actions
Function FinishPageLeave
    ; Get checkbox states
    ${NSD_GetState} $LaunchCheckboxHwnd $LaunchCheckbox
    ${NSD_GetState} $ReleaseNotesCheckboxHwnd $ReleaseNotesCheckbox
    
    ; Launch game if checkbox is checked
    ${If} $LaunchCheckbox == ${BST_CHECKED}
        ExecShell "" "$INSTDIR\Bad Suika Game.exe"
    ${EndIf}
    
    ; Open release notes if checkbox is checked
    ${If} $ReleaseNotesCheckbox == ${BST_CHECKED}
        ExecShell "open" "https://github.com/Adam-F-iguess/py-pass-proj-tres-thats-like-suika-with-help-from-HENERY"
    ${EndIf}
FunctionEnd

page directory
page instfiles
page custom FinishPage FinishPageLeave

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