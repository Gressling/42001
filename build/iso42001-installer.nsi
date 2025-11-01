; ISO 42001 AI Management System - NSIS Installer Script
; Copyright (c) 2025 Gressling Consulting GmbH, Germany E.U.

!define PRODUCT_NAME "ISO 42001 AI Management System"
!define PRODUCT_VERSION "1.0.0"
!define PRODUCT_PUBLISHER "Gressling Consulting GmbH"
!define PRODUCT_WEB_SITE "https://github.com/Gressling/42001"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\ISO42001-AIManagementSystem.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\AI Assets Management"
!define PRODUCT_UNINST_ROOT_KEY "HKCU"

; MUI 1.67 compatible ------
!include "MUI2.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "..\build\iso42001\icon\icon.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!define MUI_LICENSEPAGE_TEXT_TOP "Please review the End User License Agreement below:"
!insertmacro MUI_PAGE_LICENSE "EULA.txt"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\ISO42001-AIManagementSystem.exe"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "..\installer\ISO42001-AIManagementSystem-Setup-v${PRODUCT_VERSION}.exe"
InstallDir "$APPDATA\AI Assets Management"
InstallDirRegKey HKCU "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

; Version Information
VIProductVersion "1.0.0.0"
VIAddVersionKey "ProductName" "${PRODUCT_NAME}"
VIAddVersionKey "Comments" "Enterprise ISO 42001 AI Management System"
VIAddVersionKey "CompanyName" "${PRODUCT_PUBLISHER}"
VIAddVersionKey "LegalTrademarks" "Licensed under CC BY-NC-SA 4.0"
VIAddVersionKey "LegalCopyright" "© 2025 Gressling Consulting GmbH & Paramus Transform LLC"
VIAddVersionKey "FileDescription" "${PRODUCT_NAME} Installer"
VIAddVersionKey "FileVersion" "${PRODUCT_VERSION}"
VIAddVersionKey "ProductVersion" "${PRODUCT_VERSION}"

; Request user privileges only (no admin required)
RequestExecutionLevel user

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
  
  ; Main executable
  File "..\dist\ISO42001-AIManagementSystem.exe"
  CreateDirectory "$SMPROGRAMS\AI Assets Management"
  CreateShortCut "$SMPROGRAMS\AI Assets Management\AI Assets Management.lnk" "$INSTDIR\ISO42001-AIManagementSystem.exe"
  CreateShortCut "$DESKTOP\AI Assets Management.lnk" "$INSTDIR\ISO42001-AIManagementSystem.exe"
  
  ; Documentation
  File "..\README.md"
  File "..\LICENSE"
  File "EULA.txt"
  
  ; Create shortcuts
  ; Documentation, EULA and License shortcuts removed per user request
  
  ; Documentation folder
  SetOutPath "$INSTDIR\docs"
  File /r "..\docs\*"
  
  ; Data folder with example database
  SetOutPath "$INSTDIR\data"
  File "..\data\iso42001_example.db"
  ; Rename example database to the standard name
  Rename "$INSTDIR\data\iso42001_example.db" "$INSTDIR\data\iso42001.db"
  
  ; Configuration files
  SetOutPath "$INSTDIR"
  File "..\requirements.txt"
  File "version_info.txt"
  
SectionEnd

Section -AdditionalIcons
  CreateDirectory "$SMPROGRAMS\AI Assets Management"
  CreateShortCut "$SMPROGRAMS\AI Assets Management\Uninstall AI Assets Management.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKCU "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\ISO42001-AIManagementSystem.exe"
  WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "DisplayName" "AI Assets Management"
  WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\ISO42001-AIManagementSystem.exe"
  WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
  WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "InstallLocation" "$INSTDIR"
SectionEnd

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to uninstall AI Assets Management?" IDYES +2
  Abort
FunctionEnd

; Custom function to ask about keeping data
Function un.KeepDataDialog
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON1 "Do you want to keep your AI management data (database files)?$\n$\nSelect 'Yes' to keep your data for future use.$\nSelect 'No' to completely remove all data." IDYES keep_data
  
  ; User chose to delete data
  StrCpy $R0 "delete"
  Goto done
  
  keep_data:
  ; User chose to keep data
  StrCpy $R0 "keep"
  
  done:
FunctionEnd

Section Uninstall
  ; Ask user about keeping data
  Call un.KeepDataDialog
  
  ; Remove application files
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\ISO42001-AIManagementSystem.exe"
  Delete "$INSTDIR\README.md"
  Delete "$INSTDIR\LICENSE"
  Delete "$INSTDIR\EULA.txt"
  Delete "$INSTDIR\CHANGELOG.md"
  Delete "$INSTDIR\requirements.txt"
  Delete "$INSTDIR\version_info.txt"
  
  ; Remove documentation
  RMDir /r "$INSTDIR\docs"
  
  ; Handle data directory based on user choice
  StrCmp $R0 "delete" delete_data keep_data
  
  delete_data:
    ; Remove all data including database files
    RMDir /r "$INSTDIR\data"
    Delete "$INSTDIR\*.db"
    Delete "$INSTDIR\iso42001.db"
    MessageBox MB_ICONINFORMATION "All application data has been removed."
    Goto cleanup_shortcuts
  
  keep_data:
    ; Keep database files but remove data folder structure
    Delete "$INSTDIR\data\README.md"
    RMDir "$INSTDIR\data"
    MessageBox MB_ICONINFORMATION "Application removed but your data files have been preserved in:$\n$INSTDIR"
    Goto cleanup_shortcuts
  
  cleanup_shortcuts:
  ; Remove Start Menu shortcuts
  Delete "$SMPROGRAMS\AI Assets Management\Uninstall AI Assets Management.lnk"
  Delete "$SMPROGRAMS\AI Assets Management\AI Assets Management.lnk"
  Delete "$DESKTOP\AI Assets Management.lnk"

  RMDir "$SMPROGRAMS\AI Assets Management"
  
  ; Only remove install directory if user chose to delete data
  StrCmp $R0 "delete" remove_install_dir keep_install_dir
  
  remove_install_dir:
    RMDir "$INSTDIR"
    Goto cleanup_registry
  
  keep_install_dir:
    ; Don't remove install directory as it contains user data
    Goto cleanup_registry
  
  cleanup_registry:
  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKCU "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd