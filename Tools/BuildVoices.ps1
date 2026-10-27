param([switch]$SkipImport)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$voicePython = Join-Path $projectRoot 'Saved\TTS\venv\Scripts\python.exe'
Push-Location $projectRoot
try {
 if (!(Test-Path -LiteralPath $voicePython)) {
  python -m venv Saved/TTS/venv
  if ($LASTEXITCODE -ne 0) { throw 'Voice environment creation failed' }
 }
 & $voicePython -c 'import kokoro_onnx, soundfile, scipy'
 if ($LASTEXITCODE -ne 0) {
  & $voicePython -m pip install -r Tools/requirements-tts.txt
  if ($LASTEXITCODE -ne 0) { throw 'Voice dependency installation failed' }
 }
 & $voicePython Tools/download_tts.py
 if ($LASTEXITCODE -ne 0) { throw 'Voice model download failed' }
 & $voicePython Tools/build_voices.py
 if ($LASTEXITCODE -ne 0) { throw 'Voice generation failed' }
 if (!$SkipImport) {
  $importLog=Join-Path $projectRoot 'Saved\VoiceImport.log'
  & 'E:\UE_5.8\Engine\Binaries\Win64\UnrealEditor-Cmd.exe' "$projectRoot\CourtSimulator.uproject" "-ExecutePythonScript=$projectRoot\Tools\import_court_audio.py" -unattended -nosplash -NullRHI "-abslog=$importLog"
  if (!(Select-String -LiteralPath $importLog -Pattern 'COURT_AUDIO_IMPORT_OK' -Quiet) -or (Select-String -LiteralPath $importLog -Pattern 'LogPython: Error' -Quiet)) { throw "Audio import failed: $importLog" }
 }
} finally { Pop-Location }
