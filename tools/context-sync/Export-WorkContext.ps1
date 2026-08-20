[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Low')]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$OutputPath,

    [ValidateNotNullOrEmpty()]
    [string]$WorkspacePath = (Get-Location).Path,

    [string[]]$ContextFile = @(),

    [switch]$IncludeGitMetadata,

    [ValidateRange(1, 50)]
    [int]$RecentCommitCount = 10,

    [string]$ProjectName,

    [AllowEmptyString()]
    [string]$CurrentObjective = '',

    [AllowEmptyString()]
    [string]$NextAction = '',

    [ValidateRange(1024, 10485760)]
    [long]$MaxContextFileBytes = 1048576,

    [switch]$Force
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

function Get-AbsolutePath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$BasePath
    )

    if ([System.IO.Path]::IsPathRooted($Path)) {
        return [System.IO.Path]::GetFullPath($Path)
    }

    return [System.IO.Path]::GetFullPath((Join-Path -Path $BasePath -ChildPath $Path))
}

function Get-TextSha256 {
    param(
        [Parameter(Mandatory = $true)]
        [AllowEmptyString()]
        [string]$Text
    )

    $algorithm = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($Text)
        $hash = $algorithm.ComputeHash($bytes)
        return (($hash | ForEach-Object { $_.ToString('x2') }) -join '')
    }
    finally {
        $algorithm.Dispose()
    }
}

function Get-FileSha256 {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $algorithm = [System.Security.Cryptography.SHA256]::Create()
    $stream = [System.IO.File]::OpenRead($Path)
    try {
        $hash = $algorithm.ComputeHash($stream)
        return (($hash | ForEach-Object { $_.ToString('x2') }) -join '')
    }
    finally {
        $stream.Dispose()
        $algorithm.Dispose()
    }
}

function Assert-NoObviousSecret {
    param(
        [Parameter(Mandatory = $true)]
        [AllowEmptyString()]
        [string]$Text,

        [Parameter(Mandatory = $true)]
        [string]$DisplayName
    )

    $patterns = @(
        "(?im)^\s*[`"']?(?:password|passwd|api[_ -]?key|access[_ -]?token|refresh[_ -]?token|client[_ -]?secret|private[_ -]?key)[`"']?\s*[:=]\s*[`"']?\S{8,}",
        '(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
        '(?i)\bgh[pousr]_[A-Za-z0-9]{20,}\b',
        '(?i)\bsk-[A-Za-z0-9_-]{20,}\b',
        '(?i)\bAKIA[0-9A-Z]{16}\b',
        '(?i)\bAuthorization\s*:\s*Bearer\s+\S{12,}'
    )

    foreach ($pattern in $patterns) {
        if ($Text -match $pattern) {
            throw "Potential credential material was detected in '$DisplayName'. Remove or redact it before exporting."
        }
    }
}

function Test-SensitiveFileName {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    return $Name -match '(?i)^(?:\.env(?:\..*)?|auth(?:[._-].*)?|credentials?(?:[._-].*)?|tokens?(?:[._-].*)?|secrets?(?:[._-].*)?|passwords?(?:[._-].*)?|cookies?(?:[._-].*)?)$'
}

function Test-SensitiveGitStatusLine {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Line
    )

    # Porcelain short status begins with a two-column state plus a space
    # (for example, "?? .env" or " M path/file"). Inspect only the path
    # portion so sensitive files at the repository root are not missed.
    $pathPortion = if ($Line.Length -gt 3) { $Line.Substring(3) } else { $Line }
    $pathPortion = $pathPortion.Replace('"', '')
    $pathsToCheck = @($pathPortion -split '\s+->\s+')

    foreach ($candidatePath in $pathsToCheck) {
        if ($candidatePath.Trim() -match '(?i)(?:^|[\\/])(?:\.env(?:\.[^\\/]*)?|auth\.json(?:[._-][^\\/]*)?|\.?(?:credentials?|tokens?|secrets?|passwords?|cookies?|keys?|api[_-]?keys?|private[_-]?keys?)(?:[._-][^\\/]*)?|id_(?:rsa|dsa|ecdsa|ed25519)(?:\.[^\\/]*)?|[^\\/]+\.(?:key|pem|pfx|p12|ppk))(?:$|[\\/])') {
            return $true
        }
    }

    return $false
}

function Invoke-GitRead {
    param(
        [Parameter(Mandatory = $true)]
        [string]$GitPath,

        [Parameter(Mandatory = $true)]
        [string]$WorkingTree,

        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    $savedErrorActionPreference = $ErrorActionPreference
    $output = @()
    $exitCode = -1
    try {
        # Windows PowerShell can turn redirected native stderr into error records.
        # Suppress those records here and use the native exit code explicitly.
        $ErrorActionPreference = 'SilentlyContinue'
        $output = @(& $GitPath -C $WorkingTree @Arguments 2>$null)
        $exitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $savedErrorActionPreference
    }

    return [pscustomobject]@{
        ExitCode = $exitCode
        Output = @($output | ForEach-Object { [string]$_ })
    }
}

$workspaceItem = Get-Item -LiteralPath $WorkspacePath
if (-not $workspaceItem.PSIsContainer) {
    throw "WorkspacePath must be a directory: $WorkspacePath"
}

$workspace = $workspaceItem.FullName.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)
$workspacePrefix = $workspace + [System.IO.Path]::DirectorySeparatorChar
$currentDirectory = (Get-Location).Path
$outputFullPath = Get-AbsolutePath -Path $OutputPath -BasePath $currentDirectory
$knownArtifactNames = @('handoff.md', 'manifest.json')

if (Test-Path -LiteralPath $outputFullPath) {
    $outputItem = Get-Item -LiteralPath $outputFullPath
    if (-not $outputItem.PSIsContainer) {
        throw "OutputPath already exists as a file: $outputFullPath"
    }

    if (-not $Force) {
        throw "OutputPath already exists. Choose a new directory or pass -Force to replace only known package files: $outputFullPath"
    }

    $unexpectedItems = @(Get-ChildItem -LiteralPath $outputFullPath -Force | Where-Object { $_.Name -notin $knownArtifactNames })
    if ($unexpectedItems.Count -gt 0) {
        throw "OutputPath contains files other than handoff.md and manifest.json. Refusing to write into it: $outputFullPath"
    }
}

if ([string]::IsNullOrWhiteSpace($ProjectName)) {
    $ProjectName = Split-Path -Path $workspace -Leaf
    if ([string]::IsNullOrWhiteSpace($ProjectName)) {
        $ProjectName = 'workspace'
    }
}

Assert-NoObviousSecret -Text $CurrentObjective -DisplayName 'CurrentObjective'
Assert-NoObviousSecret -Text $NextAction -DisplayName 'NextAction'

$contextRecords = New-Object 'System.Collections.Generic.List[object]'
$contextSections = New-Object 'System.Collections.Generic.List[object]'
$seenContextPaths = @{}

foreach ($requestedContextFile in $ContextFile) {
    if ([string]::IsNullOrWhiteSpace($requestedContextFile)) {
        throw 'ContextFile entries cannot be empty.'
    }

    $candidatePath = Get-AbsolutePath -Path $requestedContextFile -BasePath $workspace
    $contextItem = Get-Item -LiteralPath $candidatePath
    if ($contextItem.PSIsContainer) {
        throw "ContextFile must be a file: $requestedContextFile"
    }

    $contextFullPath = $contextItem.FullName
    if (-not $contextFullPath.StartsWith($workspacePrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "ContextFile must be inside WorkspacePath: $requestedContextFile"
    }

    if ($seenContextPaths.ContainsKey($contextFullPath.ToLowerInvariant())) {
        continue
    }
    $seenContextPaths[$contextFullPath.ToLowerInvariant()] = $true

    $extension = $contextItem.Extension.ToLowerInvariant()
    if ($extension -notin @('.md', '.txt')) {
        throw "Only reviewable .md and .txt context files are accepted: $requestedContextFile"
    }

    if (Test-SensitiveFileName -Name $contextItem.Name) {
        throw "The context filename looks credential-related and is blocked: $requestedContextFile"
    }

    if ($contextItem.Length -gt $MaxContextFileBytes) {
        throw "ContextFile exceeds MaxContextFileBytes ($MaxContextFileBytes): $requestedContextFile"
    }

    $relativePath = $contextFullPath.Substring($workspacePrefix.Length)
    $content = [string](Get-Content -LiteralPath $contextFullPath -Raw -Encoding UTF8)
    Assert-NoObviousSecret -Text $content -DisplayName $relativePath

    $contextRecords.Add([ordered]@{
        path = $relativePath.Replace('\', '/')
        bytes = [long]$contextItem.Length
        sha256 = Get-FileSha256 -Path $contextFullPath
    })
    $contextSections.Add([pscustomobject]@{
        Path = $relativePath.Replace('\', '/')
        Content = $content
    })
}

$gitManifest = [ordered]@{
    included = $false
    scope = 'none'
}
$gitMarkdown = $null

if ($IncludeGitMetadata) {
    $gitCommand = Get-Command git -ErrorAction SilentlyContinue
    if ($null -eq $gitCommand) {
        throw 'Git was not found on PATH. Install Git or omit -IncludeGitMetadata.'
    }

    $insideResult = Invoke-GitRead -GitPath $gitCommand.Source -WorkingTree $workspace -Arguments @('rev-parse', '--is-inside-work-tree')
    $insideWorkTree = ($insideResult.Output -join "`n").Trim()
    if ($insideResult.ExitCode -ne 0 -or $insideWorkTree -ne 'true') {
        throw "WorkspacePath is not inside a Git work tree: $workspace"
    }

    $branchResult = Invoke-GitRead -GitPath $gitCommand.Source -WorkingTree $workspace -Arguments @('branch', '--show-current')
    $branch = ($branchResult.Output -join "`n").Trim()
    if ($branchResult.ExitCode -ne 0) {
        throw 'Unable to read the local Git branch.'
    }
    if ([string]::IsNullOrWhiteSpace($branch)) {
        $branch = '(detached HEAD)'
    }

    $statusResult = Invoke-GitRead -GitPath $gitCommand.Source -WorkingTree $workspace -Arguments @('status', '--short', '--branch')
    if ($statusResult.ExitCode -ne 0) {
        throw 'Unable to read local Git status.'
    }
    $statusLines = @($statusResult.Output | Where-Object { -not (Test-SensitiveGitStatusLine -Line $_) })

    $logResult = Invoke-GitRead -GitPath $gitCommand.Source -WorkingTree $workspace -Arguments @('log', '-n', [string]$RecentCommitCount, '--date=iso-strict', '--pretty=format:%H%x09%ad%x09%an%x09%s')
    $rawCommitLines = @($logResult.Output)
    if ($logResult.ExitCode -ne 0) {
        $rawCommitLines = @()
    }

    $commitRecords = New-Object 'System.Collections.Generic.List[object]'
    foreach ($rawCommitLine in $rawCommitLines) {
        $commitLine = [string]$rawCommitLine
        Assert-NoObviousSecret -Text $commitLine -DisplayName 'Git commit metadata'
        $parts = $commitLine -split "`t", 4
        if ($parts.Count -eq 4) {
            $commitRecords.Add([ordered]@{
                commit = $parts[0]
                committed_at = $parts[1]
                author = $parts[2]
                subject = $parts[3]
            })
        }
    }

    Assert-NoObviousSecret -Text ($statusLines -join "`n") -DisplayName 'Git status metadata'

    $gitManifest = [ordered]@{
        included = $true
        scope = 'local_status_and_recent_commits_only'
        branch = $branch
        status = @($statusLines)
        recent_commits = $commitRecords.ToArray()
        sensitive_status_entries_omitted = $true
        remote_urls_collected = $false
        diffs_collected = $false
    }

    $gitMarkdown = [pscustomobject]@{
        Branch = $branch
        Status = @($statusLines)
        Commits = $commitRecords.ToArray()
    }
}

$createdAtUtc = [DateTime]::UtcNow.ToString('o', [System.Globalization.CultureInfo]::InvariantCulture)
$workspaceLabel = Split-Path -Path $workspace -Leaf
if ([string]::IsNullOrWhiteSpace($workspaceLabel)) {
    $workspaceLabel = 'workspace'
}

$lines = New-Object 'System.Collections.Generic.List[string]'
[void]$lines.Add("# $ProjectName - Codex 작업 문맥 인계")
[void]$lines.Add('')
[void]$lines.Add('> 사람이 검토할 수 있는 이식 가능한 작업 문맥 자료이며, 원시 Codex 세션 백업이 아닙니다.')
[void]$lines.Add('')
[void]$lines.Add('## 인계 요약')
[void]$lines.Add('')
[void]$lines.Add("- 프로젝트: $ProjectName")
[void]$lines.Add("- 생성 시각(UTC): $createdAtUtc")
[void]$lines.Add("- 원본 workspace 이름: $workspaceLabel")
[void]$lines.Add("- Git 메타데이터 포함: $([bool]$IncludeGitMetadata)")
[void]$lines.Add('')
[void]$lines.Add('## 현재 상태')
[void]$lines.Add('')
[void]$lines.Add('### 현재 목표')
[void]$lines.Add('')
[void]$lines.Add($(if ([string]::IsNullOrWhiteSpace($CurrentObjective)) { '(전송 전에 검토하고 작성하세요.)' } else { $CurrentObjective.Trim() }))
[void]$lines.Add('')
[void]$lines.Add('### 완료 및 검증')
[void]$lines.Add('')
[void]$lines.Add('- (전송 전에 검토하고 작성하세요.)')
[void]$lines.Add('')
[void]$lines.Add('### 진행 중')
[void]$lines.Add('')
[void]$lines.Add('- (전송 전에 검토하고 작성하세요.)')
[void]$lines.Add('')
[void]$lines.Add('### 다음 행동')
[void]$lines.Add('')
[void]$lines.Add($(if ([string]::IsNullOrWhiteSpace($NextAction)) { '(전송 전에 검토하고 작성하세요.)' } else { $NextAction.Trim() }))
[void]$lines.Add('')
[void]$lines.Add('### 결정 사항, 제약 조건, 미해결 질문')
[void]$lines.Add('')
[void]$lines.Add('- (전송 전에 검토하고 작성하세요.)')
[void]$lines.Add('')
[void]$lines.Add('## 안전 경계')
[void]$lines.Add('')
[void]$lines.Add('- 프로젝트 파일은 Git/GitHub로 옮기며, 이 패키지는 작업 문맥만 전달합니다.')
[void]$lines.Add('- Codex 인증 캐시, Access Token, 비밀번호, 환경변수, 자격 증명 저장소, 원시 세션 DB, Git diff, Git Remote URL은 수집하지 않았습니다.')
[void]$lines.Add('- 다른 PC로 보내기 전에 이 Markdown 파일을 사람이 직접 검토하세요.')
[void]$lines.Add('')

if ($null -ne $gitMarkdown) {
    [void]$lines.Add('## 로컬 Git 메타데이터')
    [void]$lines.Add('')
    [void]$lines.Add("- Branch: $($gitMarkdown.Branch)")
    [void]$lines.Add('- Remote URL: 수집하지 않음')
    [void]$lines.Add('- Diff와 파일 내용: 수집하지 않음')
    [void]$lines.Add('')
    [void]$lines.Add('### 상태')
    [void]$lines.Add('')
    if ($gitMarkdown.Status.Count -eq 0) {
        [void]$lines.Add('    (표시할 수 있는 비민감 상태 항목 없음)')
    }
    else {
        foreach ($statusLine in $gitMarkdown.Status) {
            [void]$lines.Add("    $statusLine")
        }
    }
    [void]$lines.Add('')
    [void]$lines.Add('### 최근 Commit')
    [void]$lines.Add('')
    if ($gitMarkdown.Commits.Count -eq 0) {
        [void]$lines.Add('    (Commit 없음)')
    }
    else {
        foreach ($commit in $gitMarkdown.Commits) {
            [void]$lines.Add("    $($commit.commit) | $($commit.committed_at) | $($commit.author) | $($commit.subject)")
        }
    }
    [void]$lines.Add('')
}

[void]$lines.Add('## 포함된 컨텍스트 파일')
[void]$lines.Add('')
if ($contextSections.Count -eq 0) {
    [void]$lines.Add('(컨텍스트 파일이 없습니다. -ContextFile로 workspace 내부의 .md/.txt 파일을 지정하세요.)')
    [void]$lines.Add('')
}
else {
    foreach ($section in $contextSections) {
        [void]$lines.Add("### $($section.Path)")
        [void]$lines.Add('')
        foreach ($contentLine in ($section.Content -split '\r?\n')) {
            [void]$lines.Add("    $contentLine")
        }
        [void]$lines.Add('')
    }
}

[void]$lines.Add('## 받는 PC 체크리스트')
[void]$lines.Add('')
[void]$lines.Add('1. 프로젝트는 별도로 Git Pull 또는 Clone합니다.')
[void]$lines.Add('2. 수정 전에 예상 Branch와 작업 트리 상태를 확인합니다.')
[void]$lines.Add('3. 이 인계 문서를 읽고 현재 저장소 상태와 비교합니다.')
[void]$lines.Add('4. 아직 유효한 항목을 Codex에 알려 줍니다. 문서가 오래됐다면 저장소에서 확인한 사실을 우선합니다.')
[void]$lines.Add('5. 이 PC에서 Codex에 정상 로그인합니다. 다른 PC의 인증 파일은 가져오지 않습니다.')
[void]$lines.Add('')

$handoffText = ($lines -join [Environment]::NewLine) + [Environment]::NewLine
$handoffBytes = [System.Text.Encoding]::UTF8.GetBytes($handoffText)
$handoffSha256 = Get-TextSha256 -Text $handoffText

$manifest = [ordered]@{
    schema_version = 1
    package_kind = 'codex-work-context-handoff'
    created_at_utc = $createdAtUtc
    project = [ordered]@{
        name = $ProjectName
        source_workspace_label = $workspaceLabel
    }
    artifacts = @(
        [ordered]@{
            path = 'handoff.md'
            bytes = [long]$handoffBytes.Length
            sha256 = $handoffSha256
        }
    )
    context_sources = $contextRecords.ToArray()
    git = $gitManifest
    safety = [ordered]@{
        human_review_required = $true
        raw_codex_session_data_collected = $false
        authentication_files_collected = $false
        credentials_collected = $false
        environment_variables_collected = $false
        git_remote_urls_collected = $false
    }
}

$manifestText = ($manifest | ConvertTo-Json -Depth 8) + [Environment]::NewLine
Assert-NoObviousSecret -Text $manifestText -DisplayName 'generated manifest'

if ($PSCmdlet.ShouldProcess($outputFullPath, 'Create portable Codex work-context package')) {
    [void][System.IO.Directory]::CreateDirectory($outputFullPath)
    $utf8NoBom = [System.Text.UTF8Encoding]::new($false)
    [System.IO.File]::WriteAllText((Join-Path $outputFullPath 'handoff.md'), $handoffText, $utf8NoBom)
    [System.IO.File]::WriteAllText((Join-Path $outputFullPath 'manifest.json'), $manifestText, $utf8NoBom)

    [pscustomobject]@{
        PackagePath = $outputFullPath
        HandoffPath = (Join-Path $outputFullPath 'handoff.md')
        ManifestPath = (Join-Path $outputFullPath 'manifest.json')
        ContextFileCount = $contextRecords.Count
        GitMetadataIncluded = [bool]$IncludeGitMetadata
    }
}
