[CmdletBinding()]
param(
    [ValidateSet('Create', 'Validate', 'BuildNavigation')]
    [string]$Mode = 'Validate',

    [string]$ProjectPath = 'C:\URproject\drone\Drone.uproject',

    [string]$EngineRoot = 'C:\Program Files\Epic Games\UE_5.8'
)

$ErrorActionPreference = 'Stop'
$editorPath = Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor-Cmd.exe'
$pythonPath = Join-Path $PSScriptRoot 'Setup-DroneNPCGreybox.py'
$workspaceRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$runRoot = Join-Path $workspaceRoot ('.tmp-tests\npc-greybox-setup\' + [guid]::NewGuid().ToString('N'))
$userDir = Join-Path $runRoot 'User'
$logPath = Join-Path $runRoot 'Setup.log'

foreach ($requiredPath in @($editorPath, $ProjectPath, $pythonPath)) {
    if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
        throw "Required file not found: $requiredPath"
    }
}

New-Item -ItemType Directory -Path $runRoot -Force | Out-Null

if ($Mode -eq 'Validate') {
    $env:DRONE_NPC_GREYBOX_VALIDATE_ONLY = '1'
    Remove-Item Env:DRONE_NPC_GREYBOX_BUILD_NAVIGATION -ErrorAction SilentlyContinue
} elseif ($Mode -eq 'BuildNavigation') {
    Remove-Item Env:DRONE_NPC_GREYBOX_VALIDATE_ONLY -ErrorAction SilentlyContinue
    $env:DRONE_NPC_GREYBOX_BUILD_NAVIGATION = '1'
} else {
    Remove-Item Env:DRONE_NPC_GREYBOX_VALIDATE_ONLY -ErrorAction SilentlyContinue
    Remove-Item Env:DRONE_NPC_GREYBOX_BUILD_NAVIGATION -ErrorAction SilentlyContinue
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

Select-String -LiteralPath $logPath -Pattern 'DRONE_NPC_GREYBOX\|' | ForEach-Object { $_.Line }

$failed = Select-String -LiteralPath $logPath -Pattern 'DRONE_NPC_GREYBOX\|FAILED|LogPython: Error|Python script executed with errors' -Quiet
$validated = Select-String -LiteralPath $logPath -Pattern 'DRONE_NPC_GREYBOX\|VALIDATION_OK' -Quiet
$created = Select-String -LiteralPath $logPath -Pattern 'DRONE_NPC_GREYBOX\|CREATED_OK' -Quiet
$navigationBuilt = Select-String -LiteralPath $logPath -Pattern 'DRONE_NPC_GREYBOX\|NAVIGATION_OK' -Quiet

if ($editorExitCode -ne 0 -or $failed -or -not $validated) {
    throw "Drone NPC Greybox $Mode failed. Exit=$editorExitCode Log=$logPath"
}
if ($Mode -eq 'Create' -and -not $created) {
    throw "Drone NPC Greybox Create did not reach CREATED_OK. Log=$logPath"
}
if ($Mode -eq 'BuildNavigation' -and -not $navigationBuilt) {
    throw "Drone NPC Greybox BuildNavigation did not reach NAVIGATION_OK. Log=$logPath"
}

Write-Output "Drone NPC Greybox $Mode succeeded. Log=$logPath"
