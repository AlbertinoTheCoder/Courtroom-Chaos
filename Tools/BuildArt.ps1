$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
function Invoke-BlenderStage([string]$name, [string]$marker) {
  $log = Join-Path $projectRoot "Art\$name.log"
  & 'D:\Blender\blender.exe' --background --python "$projectRoot\Tools\$name.py" *> $log
  $code = $LASTEXITCODE
  # Some Blender installations fail thumbnail shutdown after successfully exporting.
  # The script's final marker is emitted only after all saves and exports finish.
  if (!(Select-String -LiteralPath $log -Pattern $marker -Quiet)) {
    Get-Content -LiteralPath $log -Tail 30
    throw "Blender stage $name failed (exit $code). See $log"
  }
  Write-Output "$name complete"
}
Invoke-BlenderStage 'build_art' 'ART_BUILD_OK'
Invoke-BlenderStage 'fix_lettering' 'LETTERING_FIXED|Lettering already corrected'
Invoke-BlenderStage 'finish_props' 'FINISH_PROPS_OK'
Invoke-BlenderStage 'build_cast' 'CAST_V2_OK'
Invoke-BlenderStage 'rig_cast' 'RIG_CAST_OK'
foreach ($stage in @('build_ui','finish_ui','build_audio')) {
  python "$projectRoot\Tools\$stage.py"
  if ($LASTEXITCODE -ne 0) { throw "Python stage $stage failed" }
}
$importLog = Join-Path $projectRoot 'Saved\ArtAssembly.log'
& 'E:\UE_5.8\Engine\Binaries\Win64\UnrealEditor-Cmd.exe' "$projectRoot\CourtSimulator.uproject" "-ExecutePythonScript=$projectRoot\Tools\assemble_unreal.py" -unattended -nosplash -NullRHI "-abslog=$importLog"
if (!(Select-String -LiteralPath $importLog -Pattern 'COURTROOM_ASSEMBLY_OK' -Quiet) -or (Select-String -LiteralPath $importLog -Pattern 'LogPython: Error' -Quiet)) { throw "Unreal assembly failed. See $importLog" }
