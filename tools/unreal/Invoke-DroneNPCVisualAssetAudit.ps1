[CmdletBinding()]
param(
    [string]$ProjectPath = 'C:\URproject\drone\Drone.uproject',
    [string]$EngineRoot = 'C:\Program Files\Epic Games\UE_5.8'
)

$ErrorActionPreference = 'Stop'
$editorPath = Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor-Cmd.exe'
$pythonPath = Join-Path $PSScriptRoot 'Audit-DroneNPCVisualAssets.py'
$workspaceRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$runRoot = Join-Path $workspaceRoot ('.tmp-tests\npc-visual-audit\' + [guid]::NewGuid().ToString('N'))
$userDir = Join-Path $runRoot 'User'
$logPath = Join-Path $runRoot 'Audit.log'

foreach ($requiredPath in @($editorPath, $ProjectPath, $pythonPath)) {
    if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
        throw "Required file not found: $requiredPath"
    }
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

& $editorPath @editorArgs
$editorExitCode = $LASTEXITCODE
if (-not (Test-Path -LiteralPath $logPath -PathType Leaf)) {
    throw "Unreal Editor did not create a log: $logPath"
}

Select-String -LiteralPath $logPath -Pattern 'DRONE_NPC_VISUAL_AUDIT\|' | ForEach-Object { $_.Line }
$failed = Select-String -LiteralPath $logPath -Pattern 'DRONE_NPC_VISUAL_AUDIT\|FAILED|LogPython: Error|Python script executed with errors' -Quiet
$completed = Select-String -LiteralPath $logPath -Pattern 'DRONE_NPC_VISUAL_AUDIT\|AUDIT_OK' -Quiet
if ($editorExitCode -ne 0 -or $failed -or -not $completed) {
    throw "Drone NPC visual asset audit failed. Exit=$editorExitCode Log=$logPath"
}

Write-Output "Drone NPC visual asset audit succeeded. Log=$logPath"
