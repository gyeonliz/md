[CmdletBinding()]
param(
    [ValidateSet('Create', 'Validate')]
    [string]$Mode = 'Validate',

    [string]$ProjectPath = 'C:\project\Drone\Drone.uproject',

    [string]$EngineRoot = 'C:\Program Files\Epic Games\UE_5.8'
)

$ErrorActionPreference = 'Stop'
$editorPath = Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor-Cmd.exe'
$pythonPath = Join-Path $PSScriptRoot 'Setup-DronePrototype.py'
$workspaceRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$runRoot = Join-Path $workspaceRoot ('.tmp-tests\unreal-prototype-setup\' + [guid]::NewGuid().ToString('N'))
$userDir = Join-Path $runRoot 'User'
$logPath = Join-Path $runRoot 'Setup.log'

if (-not (Test-Path -LiteralPath $editorPath -PathType Leaf)) {
    throw "UnrealEditor-Cmd.exe not found: $editorPath"
}
if (-not (Test-Path -LiteralPath $ProjectPath -PathType Leaf)) {
    throw "Project not found: $ProjectPath"
}
if (-not (Test-Path -LiteralPath $pythonPath -PathType Leaf)) {
    throw "Setup script not found: $pythonPath"
}

New-Item -ItemType Directory -Path $runRoot -Force | Out-Null

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

if ($Mode -eq 'Validate') {
    $env:DRONE_PROTOTYPE_VALIDATE_ONLY = '1'
} else {
    Remove-Item Env:DRONE_PROTOTYPE_VALIDATE_ONLY -ErrorAction SilentlyContinue
}

& $editorPath @editorArgs
$editorExitCode = $LASTEXITCODE

if (-not (Test-Path -LiteralPath $logPath -PathType Leaf)) {
    throw "Unreal Editor did not create a log: $logPath"
}

$failure = Select-String -LiteralPath $logPath -Pattern 'DRONE_SETUP\|FAILED|LogPython: Error|Python script executed with errors' -Quiet
$validationOk = Select-String -LiteralPath $logPath -Pattern 'DRONE_SETUP\|VALIDATION_OK' -Quiet
$creationOk = Select-String -LiteralPath $logPath -Pattern 'DRONE_SETUP\|CREATED_OK' -Quiet

Select-String -LiteralPath $logPath -Pattern 'DRONE_SETUP\|' | ForEach-Object { $_.Line }

if ($editorExitCode -ne 0 -or $failure -or -not $validationOk) {
    throw "Drone Prototype $Mode failed. Exit=$editorExitCode Log=$logPath"
}
if ($Mode -eq 'Create' -and -not $creationOk) {
    throw "Drone Prototype Create did not reach CREATED_OK. Log=$logPath"
}

Write-Output "Drone Prototype $Mode succeeded. Log=$logPath"
