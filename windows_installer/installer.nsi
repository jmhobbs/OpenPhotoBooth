;--------------------------------
; Includes

	!include "MUI2.nsh" ; For Modern UI

;--------------------------------
; General

	; Name of installer and output file name
	Name "OpenPhotoBooth"
	OutFile "OpenPhotoBoothInstaller.exe"

	; Set the compressor to the LZMA for best packing
	SetCompressor /FINAL lzma

	; The little line displayed during actual installation
	BrandingText " "

	; Default installation folder
	InstallDir "$PROGRAMFILES\OpenPhotoBooth"

	; Get installation folder from registry if available
	InstallDirRegKey HKCU "Software\OpenPhotoBooth" ""

	; Request application privileges for Windows Vista
	RequestExecutionLevel admin

;--------------------------------
; Interface Configuration

	!define MUI_HEADERIMAGE
	;!define MUI_HEADERIMAGE_BITMAP "graphics\header.bmp"
	;!define MUI_HEADERIMAGE_UNBITMAP "graphics\header.bmp"

	!define MUI_ABORTWARNING

	!define MUI_ICON "graphics\install.ico"
	!define MUI_UNICON "graphics\uninstall.ico"


	;!define MUI_WELCOMEFINISHPAGE_BITMAP "graphics\instWelcome.bmp" ; 164x314
	;!define MUI_UNWELCOMEFINISHPAGE_BITMAP "graphics\uninstWelcome.bmp" ; 164x314

;--------------------------------
; Pages

	!insertmacro MUI_PAGE_WELCOME
	!insertmacro MUI_PAGE_LICENSE "../app/LICENSE"
	!insertmacro MUI_PAGE_COMPONENTS
	!insertmacro MUI_PAGE_DIRECTORY
	!insertmacro MUI_PAGE_INSTFILES
	!insertmacro MUI_PAGE_FINISH

	!insertmacro MUI_UNPAGE_WELCOME
	!insertmacro MUI_UNPAGE_CONFIRM
	!insertmacro MUI_UNPAGE_INSTFILES
	!insertmacro MUI_UNPAGE_FINISH

;--------------------------------
; Languages

	!insertmacro MUI_LANGUAGE "English"

;--------------------------------
; Installer Sections


Section "Application" SecApp

	; This says it _must_ be an installed section
	SectionIn RO

	SetOutPath "$INSTDIR"

	; Load everything as is in the build folder
	File /r "build\*"

	; Store installation folder
	WriteRegStr HKCU "Software\OpenPhotoBooth" "" $INSTDIR

	; Write the uninstall keys for Windows Add/Remove Programs App
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\OpenPhotoBooth" "DisplayName" "OpenPhotoBooth"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\OpenPhotoBooth" "UninstallString" '"$INSTDIR\uninstall.exe"'
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\OpenPhotoBooth" "NoModify" 1
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\OpenPhotoBooth" "NoRepair" 1

	; Create uninstaller
	WriteUninstaller "$INSTDIR\uninstall.exe"

SectionEnd

Section "Start Menu Shortcuts" SecSM

	; Setting this sets the working directory for the shortcuts created below
	SetOutPath "$INSTDIR"

	CreateDirectory "$SMPROGRAMS\OpenPhotoBooth"
	CreateShortCut "$SMPROGRAMS\OpenPhotoBooth\uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
	CreateShortCut "$SMPROGRAMS\OpenPhotoBooth\OpenPhotoBooth.lnk" "$INSTDIR\bin\OpenPhotoBooth.exe" "" "$INSTDIR\bin\OpenPhotoBooth.exe" 0

SectionEnd

;--------------------------------
; Descriptions

	; Language strings
	LangString DESC_SecApp ${LANG_ENGLISH} "The OpenPhotoBooth Application"
	LangString DESC_SecSM ${LANG_ENGLISH} "Application shortcuts for the Start Menu"

	; Assign language strings to sections
	!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
		!insertmacro MUI_DESCRIPTION_TEXT ${SecApp} $(DESC_SecApp)
		!insertmacro MUI_DESCRIPTION_TEXT ${SecSM} $(DESC_SecSM)
	!insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
; Uninstaller Section

Section "Uninstall"

	; Remove our files
	RMDir /r "$INSTDIR"

	; Remove shortcuts
	RMDir /r "$SMPROGRAMS\OpenPhotoBooth"

	; Clean up registry
	DeleteRegKey HKCU "Software\OpenPhotoBooth"
	DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\OpenPhotoBooth"

SectionEnd