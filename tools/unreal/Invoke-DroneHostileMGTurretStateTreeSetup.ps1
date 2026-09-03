[CmdletBinding()]
param(
    [ValidateSet('Upgrade', 'Validate')]
    [string]$Mode = 'Validate',

    [string]$ProjectPath = 'D:\JGY\project\drone\Drone.uproject',

    [string]$EngineRoot = 'C:\Program Files\Epic Games\UE_5.8'
)

$ErrorActionPreference = 'Stop'
$editorPath = Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor-Cmd.exe'
$pythonPath = Join-Path $PSScriptRoot 'Setup-DroneHostileMGTurretStateTree.py'
$workspaceRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$runRoot = Join-Path $workspaceRoot ('.tmp-tests\hostile-mg-statetree\' + [guid]::NewGuid().ToString('N'))
$userDir = Join-Path $runRoot 'User'
$logPath = Join-Path $runRoot 'Setup.log'

foreach ($requiredPath in @($editorPath, $ProjectPath, $pythonPath)) {
    if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
        throw "Required file not found: $requiredPath"
    }
}

New-Item -ItemType Directory -Path $runRoot -Force | Out-Null
if ($Mode -eq 'Validate') {
    $env:DRONE_HOSTILE_MG_VALIDATE_ONLY = '1'
} else {
    Remove-Item Env:DRONE_HOSTILE_MG_VALIDATE_ONLY -ErrorAction SilentlyContinue
}

$editorArgs = @(
    $ProjectPath,
    '-unattended',
    '-nop4',
    '-nullrhi',
    '-nosound',
    '-nosplash',
    '-NoAssetRegistryCache',
    '-EnablePlugins=PythonScriptPlugin',
    '-ScriptErrorsAreFatal',
    ('-ExecutePythonScript=' + $pythonPath),
    ('-UserDir=' + $userDir),
    ('-abslog=' + $logPath)
)

& $editorPath @editorArgs
$editorExitCode = $LASTEXITCODE
if (-not (Test-Path -LiteralPath $logPath -PathType Leaf)) {
    throw "Unreal Editor did not create a log: $logPath"
}

Select-String -LiteralPath $logPath -Pattern 'DRONE_HOSTILE_MG\|' | ForEach-Object { $_.Line }
$failed = Select-String -LiteralPath $logPath -Pattern 'DRONE_HOSTILE_MG\|FAILED|LogPython: Error|Python script executed with errors' -Quiet
$validated = Select-String -LiteralPath $logPath -Pattern 'DRONE_HOSTILE_MG\|VALIDATION_OK' -Quiet
$upgraded = Select-String -LiteralPath $logPath -Pattern 'DRONE_HOSTILE_MG\|UPGRADE_OK' -Quiet

if ($editorExitCode -ne 0 -or $failed -or -not $validated) {
    throw "Drone hostile MG StateTree $Mode failed. Exit=$editorExitCode Log=$logPath"
}
if ($Mode -eq 'Upgrade' -and -not $upgraded) {
    throw "Drone hostile MG StateTree Upgrade did not reach UPGRADE_OK. Log=$logPath"
}

Write-Output "Drone hostile MG StateTree $Mode succeeded. Log=$logPath"
