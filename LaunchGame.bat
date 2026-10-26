@echo off
cd /d "%~dp0"
if exist "%~dp0Builds\Windows\CourtSimulator.exe" (
  start "Courtroom Chaos" "%~dp0Builds\Windows\CourtSimulator.exe" -windowed -ResX=1280 -ResY=720
  exit /b
)
"E:\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe" "%~dp0CourtSimulator.uproject" -game -windowed -ResX=1280 -ResY=720 -log
