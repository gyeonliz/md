[CmdletBinding()]
param(
    [ValidateSet('Create', 'Validate')]
    [string]$Mode = 'Validate',

    [string]$ProjectPath = '',

    [string]$EngineRoot = 'C:\Program Files\Epic Games\UE_5.8'
)

$ErrorActionPreference = 'Stop'
$editorPath = Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor-Cmd.exe'
$pythonPath = Join-Path $PSScriptRoot 'Setup-DroneSmartObjectStations.py'
$workspaceRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
if ([string]::IsNullOrWhiteSpace($ProjectPath)) {
    $projectRoot = Join-Path (Split-Path $workspaceRoot -Parent) 'drone'
    $ProjectPath = Join-Path $projectRoot 'Drone.uproject'
}
$runRoot = Join-Path $workspaceRoot ('.tmp-tests\smart-object-setup\' + [guid]::NewGuid().ToString('N'))
$userDir = Join-Path $runRoot 'User'
$logPath = Join-Path $runRoot 'Setup.log'

foreach ($requiredPath in @($editorPath, $ProjectPath, $pythonPath)) {
    if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
        throw "Required file not found: $requiredPath"
    }
}

New-Item -ItemType Directory -Path $runRoot -Force | Out-Null

if ($Mode -eq 'Validate') {
    $env:DRONE_SMART_OBJECT_VALIDATE_ONLY = '1'
} else {
    Remove-Item Env:DRONE_SMART_OBJECT_VALIDATE_ONLY -ErrorAction SilentlyContinue
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

Select-String -LiteralPath $logPath -Pattern 'DRONE_SO_SETUP\|' | ForEach-Object { $_.Line }

$failed = Select-String -LiteralPath $logPath -Pattern 'DRONE_SO_SETUP\|FAILED|LogPython: Error|Python script executed with errors' -Quiet
$validated = Select-String -LiteralPath $logPath -Pattern 'DRONE_SO_SETUP\|VALIDATION_OK' -Quiet
$created = Select-String -LiteralPath $logPath -Pattern 'DRONE_SO_SETUP\|CREATED_OK' -Quiet

if ($editorExitCode -ne 0 -or $failed -or -not $validated) {
    throw "Drone Smart Object $Mode failed. Exit=$editorExitCode Log=$logPath"
}
if ($Mode -eq 'Create' -and -not $created) {
    throw "Drone Smart Object Create did not reach CREATED_OK. Log=$logPath"
}

Write-Output "Drone Smart Object $Mode succeeded. Log=$logPath"
