#define Name "Corkscrew"
#define Version "#VERSION#"
#define Publisher "androidWG"
#define InfoURL "https://github.com/androidWG/Corkscrew"
#define LocalPath "#REPO#"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{79629986-A73C-425E-B426-60C4F9EC7823}
AppName={#Name}
AppVersion={#Version}
;AppVerName={#Name} {#Version}
AppPublisher={#Publisher}
AppPublisherURL={#InfoURL}
AppSupportURL={#InfoURL}
AppUpdatesURL={#InfoURL}
DefaultDirName={localappdata}\Programs\{#Name}
DisableProgramGroupPage=yes
AllowNoIcons=yes
OutputDir={#LocalPath}\dist
OutputBaseFilename=corkscrew-win-#VERSION#
SetupIconFile={#LocalPath}\resources\icon.ico
Compression=lzma
SolidCompression=yes
UninstallDisplayName=Corkscrew Updater
UninstallDisplayIcon={#LocalPath}\resources\icon.ico
MinVersion=0,6.1
WizardStyle=modern
WizardSizePercent=100
RestartIfNeededByRun=False
VersionInfoVersion={#Version}
VersionInfoDescription=A background updater for OpenRCT2
VersionInfoProductName=Corkscrew
VersionInfoProductVersion={#Version}
WizardImageFile={#LocalPath}\build\resources\banner_0.59x.bmp , {#LocalPath}\build\resources\banner_0.5x.bmp , {#LocalPath}\build\resources\banner_0.75x.bmp , {#LocalPath}\build\resources\banner_0.83x.bmp , {#LocalPath}\build\resources\banner_1.25x.bmp , {#LocalPath}\build\resources\banner_1.5x.bmp , {#LocalPath}\build\resources\banner_1x.bmp
WizardSmallImageFile={#LocalPath}\build\resources\banner_small_0.59x.bmp , {#LocalPath}\build\resources\banner_small_0.5x.bmp , {#LocalPath}\build\resources\banner_small_0.75x.bmp , {#LocalPath}\build\resources\banner_small_0.83x.bmp , {#LocalPath}\build\resources\banner_small_1.25x.bmp , {#LocalPath}\build\resources\banner_small_1.5x.bmp , {#LocalPath}\build\resources\banner_small_1x.bmp

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "{#LocalPath}\dist\Corkscrew.exe"; DestDir: "{app}"; Flags: ignoreversion

[Run]
Filename: "schtasks"; Parameters: "/Create /F /TN ""Corkscrew Updater"" /TR ""{app}\Corkscrew.exe"" /SC HOURLY /MO 4"; Flags: runhidden

[UninstallRun]
Filename: "schtasks"; Parameters: "/Delete /TN ""Corkscrew Updater"" /F"; Flags: runhidden

[ThirdParty]
CompileLogFile={#LocalPath}\dist\{#Version}-installer.log
