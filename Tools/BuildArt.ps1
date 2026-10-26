$projectRoot = Split-Path $PSScriptRoot -Parent
& 'D:\Blender\blender.exe' --background --python "$projectRoot\Tools\build_art.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& 'D:\Blender\blender.exe' --background --python "$projectRoot\Tools\fix_lettering.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& 'D:\Blender\blender.exe' --background --python "$projectRoot\Tools\build_cast.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& 'D:\Blender\blender.exe' --background --python "$projectRoot\Tools\rig_cast.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$projectRoot\Tools\build_ui.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$projectRoot\Tools\build_audio.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& 'E:\UE_5.8\Engine\Binaries\Win64\UnrealEditor-Cmd.exe' "$projectRoot\CourtSimulator.uproject" "-ExecutePythonScript=$projectRoot\Tools\assemble_unreal.py" -unattended -nosplash
