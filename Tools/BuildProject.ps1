$projectRoot = Split-Path $PSScriptRoot -Parent
& 'E:\UE_5.8\Engine\Build\BatchFiles\Build.bat' CourtSimulatorEditor Win64 Development "-Project=$projectRoot\CourtSimulator.uproject" -WaitMutex -NoHotReloadFromIDE -NoUBA -MaxParallelActions=2
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
