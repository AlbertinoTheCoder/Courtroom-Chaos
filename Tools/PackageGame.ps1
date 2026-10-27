$projectRoot = Split-Path $PSScriptRoot -Parent
& 'E:\UE_5.8\Engine\Build\BatchFiles\RunUAT.bat' BuildCookRun "-project=$projectRoot\CourtSimulator.uproject" -WaitForUATMutex -noP4 -platform=Win64 -clientconfig=Development -build -cook -stage -pak -archive "-archivedirectory=$projectRoot\Builds" -utf8output -unattended -nocompileeditor "-ubtargs=-NoUBA -nocache -UBARootDir=$projectRoot\Saved\UBA -MaxParallelActions=2"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
