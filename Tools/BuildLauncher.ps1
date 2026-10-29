$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$compiler = Join-Path $env:WINDIR 'Microsoft.NET/Framework64/v4.0.30319/csc.exe'
if (!(Test-Path -LiteralPath $compiler)) { throw 'The Windows .NET Framework C# compiler is required.' }
$launcherSource = Join-Path $PSScriptRoot 'Launcher\Program.cs'
$launcherExe = Join-Path $projectRoot 'CourtroomChaos.exe'
& $compiler /nologo /target:winexe /optimize+ /reference:System.Windows.Forms.dll "/out:$launcherExe" $launcherSource
if ($LASTEXITCODE -ne 0) { throw 'Launcher build failed.' }
$check = Start-Process -FilePath "$projectRoot/CourtroomChaos.exe" -ArgumentList '--check' -PassThru -WindowStyle Hidden
$check.WaitForExit()
if ($check.ExitCode -ne 0) { throw 'Launcher built, but the packaged runtime is missing. Run PackageGame.ps1 first.' }
Write-Output 'Launcher build and runtime-path check passed.'
