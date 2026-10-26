$projectRoot = Split-Path $PSScriptRoot -Parent
$report = Join-Path $projectRoot 'Saved\TrialTest.txt'
if (Test-Path -LiteralPath $report) { Remove-Item -LiteralPath $report }
$animationReport = Join-Path $projectRoot 'Saved\AnimationTest.txt'
if (Test-Path -LiteralPath $animationReport) { Remove-Item -LiteralPath $animationReport }
$testArgs = @("$projectRoot\CourtSimulator.uproject", '/Game/Courtroom/L_Courtroom', '-game', '-RenderOffscreen', '-ResX=1280', '-ResY=720', '-CourtSelfTest', '-unattended', '-nosplash', "-abslog=$projectRoot\Saved\TestRun.log")
$testProcess = Start-Process -FilePath 'E:\UE_5.8\Engine\Binaries\Win64\UnrealEditor-Cmd.exe' -ArgumentList $testArgs -PassThru -WindowStyle Hidden
$deadline = (Get-Date).AddSeconds(120)
try {
  while (!(Test-Path -LiteralPath $report) -or !(Test-Path -LiteralPath $animationReport)) {
    if ($testProcess.HasExited) { throw 'Test runtime exited before producing both reports.' }
    if ((Get-Date) -gt $deadline) { throw 'Test runtime timed out.' }
    Start-Sleep -Milliseconds 250
  }
  foreach ($path in @($report, $animationReport)) {
    $result = Get-Content -LiteralPath $path -Raw
    Write-Output $result
    if (!$result.StartsWith('PASS:')) { throw "Integration test failed: $path" }
  }
} finally {
  if (!$testProcess.HasExited) { Stop-Process -Id $testProcess.Id }
}
