[CmdletBinding()]
param(
    [string]$DocsPath = ([System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))),
    [string]$DroneProjectPath = 'D:\JGY\project\drone\Drone.uproject',
    [string]$EngineRoot = 'C:\Program Files\Epic Games\UE_5.8',
    [switch]$RequireClean,
    [switch]$RunLfsFsck,
    [switch]$RunBuild,
    [switch]$RunTutorialValidation
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

$failures = New-Object 'System.Collections.Generic.List[string]'
$warnings = New-Object 'System.Collections.Generic.List[string]'

function Write-Check {
    param(
        [Parameter(Mandatory)][ValidateSet('PASS', 'WARN', 'FAIL')][string]$State,
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][string]$Detail
    )

    Write-Output ("[{0}] {1}: {2}" -f $State, $Name, $Detail)
    if ($State -eq 'WARN') {
        $warnings.Add("${Name}: $Detail")
    }
    elseif ($State -eq 'FAIL') {
        $failures.Add("${Name}: $Detail")
    }
}

function Invoke-ExternalRead {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [Parameter(Mandatory)][string[]]$Arguments
    )

    $oldPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'Continue'
        $output = @(& $FilePath @Arguments 2>&1 | ForEach-Object { [string]$_ })
        $exitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $oldPreference
    }

    return [pscustomobject]@{
        ExitCode = $exitCode
        Output = $output
        Text = ($output -join "`n").Trim()
    }
}

function Test-LfsPointerPlaceholder {
    param([Parameter(Mandatory)][string]$Path)

    $stream = [System.IO.File]::OpenRead($Path)
    try {
        $buffer = New-Object byte[] 64
        $count = $stream.Read($buffer, 0, $buffer.Length)
        $prefix = [System.Text.Encoding]::ASCII.GetString($buffer, 0, $count)
        return $prefix.StartsWith('version https://git-lfs.github.com/spec/v1')
    }
    finally {
        $stream.Dispose()
    }
}

function Test-GitRepository {
    param(
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$GitPath
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        Write-Check FAIL $Name "Repository directory not found: $Path"
        return
    }

    $inside = Invoke-ExternalRead $GitPath @('-C', $Path, 'rev-parse', '--is-inside-work-tree')
    if ($inside.ExitCode -ne 0 -or $inside.Text -ne 'true') {
        Write-Check FAIL $Name "Not a Git repository: $Path"
        return
    }

    $branch = Invoke-ExternalRead $GitPath @('-C', $Path, 'branch', '--show-current')
    if ($branch.ExitCode -ne 0) {
        Write-Check FAIL "$Name Branch" 'Unable to read the current branch.'
    }
    elseif ($branch.Text -eq 'main') {
        Write-Check PASS "$Name Branch" 'main'
    }
    else {
        Write-Check WARN "$Name Branch" "Current branch is not main: $($branch.Text)"
    }

    $upstream = Invoke-ExternalRead $GitPath @('-C', $Path, 'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}')
    if ($upstream.ExitCode -ne 0) {
        Write-Check FAIL "$Name Upstream" 'No tracked upstream branch.'
    }
    else {
        $counts = Invoke-ExternalRead $GitPath @('-C', $Path, 'rev-list', '--left-right', '--count', 'HEAD...@{u}')
        if ($counts.ExitCode -ne 0 -or $counts.Text -notmatch '^(\d+)\s+(\d+)$') {
            Write-Check FAIL "$Name Sync" 'Unable to compare HEAD with upstream.'
        }
        else {
            $ahead = [int]$Matches[1]
            $behind = [int]$Matches[2]
            if ($behind -gt 0) {
                Write-Check FAIL "$Name Sync" "Local branch is $behind commit(s) behind upstream. Fetch and pull."
            }
            elseif ($ahead -gt 0) {
                Write-Check WARN "$Name Sync" "Local branch is $ahead commit(s) ahead of upstream. Push to share it."
            }
            else {
                Write-Check PASS "$Name Sync" "HEAD matches $($upstream.Text)."
            }
        }
    }

    $status = Invoke-ExternalRead $GitPath @('-C', $Path, 'status', '--porcelain')
    if ($status.ExitCode -ne 0) {
        Write-Check FAIL "$Name Worktree" 'Unable to read worktree status.'
    }
    elseif ([string]::IsNullOrWhiteSpace($status.Text)) {
        Write-Check PASS "$Name Worktree" 'Clean'
    }
    elseif ($RequireClean) {
        Write-Check FAIL "$Name Worktree" 'Local changes exist. Confirm ownership before starting new work.'
    }
    else {
        Write-Check WARN "$Name Worktree" 'Local changes exist. Do not discard or delete them automatically.'
    }
}

$gitCommand = Get-Command git -ErrorAction SilentlyContinue
if ($null -eq $gitCommand) {
    Write-Check FAIL 'Git' 'git.exe was not found on PATH.'
}
else {
    $gitVersion = Invoke-ExternalRead $gitCommand.Source @('--version')
    Write-Check PASS 'Git' $gitVersion.Text

    $lfsVersion = Invoke-ExternalRead $gitCommand.Source @('lfs', 'version')
    if ($lfsVersion.ExitCode -eq 0) {
        Write-Check PASS 'Git LFS' $lfsVersion.Text
    }
    else {
        Write-Check FAIL 'Git LFS' 'Git LFS is not installed.'
    }
}

$docsFullPath = [System.IO.Path]::GetFullPath($DocsPath)
$projectFullPath = [System.IO.Path]::GetFullPath($DroneProjectPath)
$droneRoot = Split-Path -Path $projectFullPath -Parent
$engineFullPath = [System.IO.Path]::GetFullPath($EngineRoot)
$buildPath = Join-Path $engineFullPath 'Engine\Build\BatchFiles\Build.bat'
$editorCmdPath = Join-Path $engineFullPath 'Engine\Binaries\Win64\UnrealEditor-Cmd.exe'

if ($null -ne $gitCommand) {
    Test-GitRepository -Name 'Docs Repository' -Path $docsFullPath -GitPath $gitCommand.Source
    Test-GitRepository -Name 'Unreal Repository' -Path $droneRoot -GitPath $gitCommand.Source
}

if (Test-Path -LiteralPath $projectFullPath -PathType Leaf) {
    Write-Check PASS 'Unreal Project' $projectFullPath
    try {
        $projectJson = Get-Content -LiteralPath $projectFullPath -Raw -Encoding UTF8 | ConvertFrom-Json
        if ([string]$projectJson.EngineAssociation -like '5.8*') {
            Write-Check PASS 'Engine Association' ([string]$projectJson.EngineAssociation)
        }
        else {
            Write-Check WARN 'Engine Association' "Expected UE 5.8 family, found: $($projectJson.EngineAssociation)"
        }

        $requiredPlugins = @('StateTree', 'GameplayStateTree', 'SmartObjects', 'GameplayInteractions')
        $enabledPluginNames = @($projectJson.Plugins | Where-Object { $_.Enabled } | ForEach-Object { [string]$_.Name })
        $missingPlugins = @($requiredPlugins | Where-Object { $_ -notin $enabledPluginNames })
        if ($missingPlugins.Count -eq 0) {
            Write-Check PASS 'Runtime Plugins' ($requiredPlugins -join ', ')
        }
        else {
            Write-Check FAIL 'Runtime Plugins' ("Missing enabled uproject plugins: " + ($missingPlugins -join ', '))
        }
    }
    catch {
        Write-Check FAIL 'uproject JSON' $_.Exception.Message
    }
}
else {
    Write-Check FAIL 'Unreal Project' "File not found: $projectFullPath"
}

if (Test-Path -LiteralPath $buildPath -PathType Leaf) {
    Write-Check PASS 'Unreal Build Tool' $buildPath
}
else {
    Write-Check FAIL 'Unreal Build Tool' "File not found: $buildPath"
}
if (Test-Path -LiteralPath $editorCmdPath -PathType Leaf) {
    Write-Check PASS 'Unreal Editor Cmd' $editorCmdPath
}
else {
    Write-Check FAIL 'Unreal Editor Cmd' "File not found: $editorCmdPath"
}

$requiredAssets = @(
    'Content\Drone\Maps\TestMap\Lvl_DroneTutorialMissionTest.umap',
    'Content\Drone\Mission\Blueprints\Tutorial\BP_TutorialHoverZone.uasset',
    'Content\Drone\Mission\Blueprints\Tutorial\BP_TutorialHeadingZone.uasset',
    'Content\Drone\Data\Missions\DA_Mission_Tutorial_Hover.uasset',
    'Content\Drone\Data\Missions\DA_Mission_Tutorial_Forward.uasset',
    'Content\Drone\Data\Missions\DA_Mission_Tutorial_Heading.uasset',
    'Content\Drone\Data\Missions\DA_Mission_Tutorial_GateFlight.uasset',
    'Content\Drone\Data\Missions\DA_Mission_Tutorial_FPV.uasset',
    'Content\Drone\Data\Missions\DA_Mission_Tutorial_Payload.uasset',
    'Content\Drone\Data\Missions\DA_Mission_Tutorial_UGV_NPC.uasset',
    'Content\Drone\Data\Missions\DA_Mission_Tutorial_UGV_Turret.uasset'
)
$missingAssets = New-Object 'System.Collections.Generic.List[string]'
$pointerAssets = New-Object 'System.Collections.Generic.List[string]'
foreach ($relativeAsset in $requiredAssets) {
    $assetPath = Join-Path $droneRoot $relativeAsset
    if (-not (Test-Path -LiteralPath $assetPath -PathType Leaf)) {
        $missingAssets.Add($relativeAsset)
    }
    elseif (Test-LfsPointerPlaceholder -Path $assetPath) {
        $pointerAssets.Add($relativeAsset)
    }
}
if ($missingAssets.Count -gt 0) {
    Write-Check FAIL 'Tutorial Assets' ("Missing: " + ($missingAssets -join ', '))
}
elseif ($pointerAssets.Count -gt 0) {
    Write-Check FAIL 'Tutorial Assets' ("LFS content was not downloaded: " + ($pointerAssets -join ', '))
}
else {
    Write-Check PASS 'Tutorial Assets' 'Shared map, Hover/Heading blueprints, and eight mission definitions are present.'
}

if ($RunLfsFsck -and $null -ne $gitCommand -and (Test-Path -LiteralPath $droneRoot -PathType Container)) {
    $lfsFsck = Invoke-ExternalRead $gitCommand.Source @('-C', $droneRoot, 'lfs', 'fsck', '--pointers', 'HEAD')
    if ($lfsFsck.ExitCode -eq 0) {
        Write-Check PASS 'Git LFS Fsck' $(if ($lfsFsck.Text) { $lfsFsck.Text } else { 'Passed' })
    }
    else {
        Write-Check FAIL 'Git LFS Fsck' $lfsFsck.Text
    }
}

$unrealProcesses = @(Get-Process UnrealEditor, UnrealEditor-Cmd -ErrorAction SilentlyContinue)
if (($RunBuild -or $RunTutorialValidation) -and $unrealProcesses.Count -gt 0) {
    Write-Check FAIL 'Unreal Process' 'Save and close Unreal Editor before build or validation.'
}

if ($RunBuild -and $unrealProcesses.Count -eq 0 -and (Test-Path -LiteralPath $buildPath -PathType Leaf)) {
    & $buildPath DroneEditor Win64 Development $projectFullPath -WaitMutex -NoHotReloadFromIDE
    if ($LASTEXITCODE -eq 0) {
        Write-Check PASS 'DroneEditor Build' 'Win64 Development succeeded.'
    }
    else {
        Write-Check FAIL 'DroneEditor Build' "Exit=$LASTEXITCODE"
    }
}

if ($RunTutorialValidation -and $unrealProcesses.Count -eq 0 -and (Test-Path -LiteralPath $editorCmdPath -PathType Leaf)) {
    $validationScript = Join-Path $droneRoot 'Tools\AssetMigration\Invoke-DroneTutorialMissionTest.ps1'
    if (-not (Test-Path -LiteralPath $validationScript -PathType Leaf)) {
        Write-Check FAIL 'Tutorial Validation' "Script not found: $validationScript"
    }
    else {
        & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $validationScript -Mode Validate -ProjectPath $projectFullPath -EngineRoot $engineFullPath
        if ($LASTEXITCODE -eq 0) {
            Write-Check PASS 'Tutorial Validation' 'Map Check and eight-mission asset contract passed.'
        }
        else {
            Write-Check FAIL 'Tutorial Validation' "Exit=$LASTEXITCODE"
        }
    }
}

Write-Output ''
Write-Output ("Check summary: {0} failure(s), {1} warning(s)" -f $failures.Count, $warnings.Count)
if ($warnings.Count -gt 0) {
    $warnings | ForEach-Object { Write-Output ("WARN: " + $_) }
}
if ($failures.Count -gt 0) {
    $failures | ForEach-Object { Write-Output ("FAIL: " + $_) }
    throw 'Workstation readiness check failed. Resolve the FAIL items and run it again.'
}

Write-Output 'WORKSTATION_READY'
