param([switch]$Packaged)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$reportRoot = Join-Path $projectRoot 'Saved'
$executable = 'E:\UE_5.8\Engine\Binaries\Win64\UnrealEditor-Cmd.exe'
$testArgs = @("$projectRoot\CourtSimulator.uproject", '/Game/Courtroom/L_Courtroom')
if ($Packaged) {
  $executable = Join-Path $projectRoot 'Builds\Windows\CourtSimulator\Binaries\Win64\CourtSimulator.exe'
  if (!(Test-Path -LiteralPath $executable)) { throw 'Package the game first.' }
  $testUser = Join-Path $projectRoot 'Saved\PackagedVerification'
  $reportRoot = Join-Path $testUser 'Saved'
  $testArgs = @("-UserDir=$testUser/")
}
$reports = @('TrialTest.txt','AnimationTest.txt','ChoreographyTest.txt','AudioTest.txt') | ForEach-Object { Join-Path $reportRoot $_ }
foreach ($path in $reports) { if (Test-Path -LiteralPath $path) { Remove-Item -LiteralPath $path } }
$testArgs += @('-game','-RenderOffscreen','-ResX=1280','-ResY=720','-CourtSelfTest','-unattended','-nosplash',"-abslog=$projectRoot\Saved\$(if ($Packaged) {'PackagedTest'} else {'TestRun'}).log")
$testProcess = Start-Process -FilePath $executable -ArgumentList $testArgs -PassThru -WindowStyle Hidden
$deadline = (Get-Date).AddMinutes(10)
try {
  while (@($reports | Where-Object { !(Test-Path -LiteralPath $_) }).Count -gt 0) {
    if ($testProcess.HasExited) { throw 'Test runtime exited before producing all required reports.' }
    if ((Get-Date) -gt $deadline) { throw 'Test runtime timed out.' }
    Start-Sleep -Milliseconds 250
  }
  foreach ($path in $reports) {
    $result = Get-Content -LiteralPath $path -Raw
    Write-Output $result
    if (!$result.StartsWith('PASS:')) { throw "Integration test failed: $path" }
  }
} finally {
  if (!$testProcess.HasExited) { Stop-Process -Id $testProcess.Id }
}
