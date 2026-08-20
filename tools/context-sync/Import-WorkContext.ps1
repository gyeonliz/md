[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Low')]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$PackagePath,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$DestinationPath,

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
            throw "Potential credential material was detected in '$DisplayName'. Refusing to import the package."
        }
    }
}

$currentDirectory = (Get-Location).Path
$packageItem = Get-Item -LiteralPath $PackagePath
if (-not $packageItem.PSIsContainer) {
    throw "PackagePath must be a directory: $PackagePath"
}

$packageFullPath = $packageItem.FullName.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)
$knownArtifactNames = @('handoff.md', 'manifest.json')
$unexpectedPackageItems = @(Get-ChildItem -LiteralPath $packageFullPath -Force | Where-Object { $_.Name -notin $knownArtifactNames })
if ($unexpectedPackageItems.Count -gt 0) {
    throw "Package contains unexpected files. Only handoff.md and manifest.json are accepted: $packageFullPath"
}

$handoffPath = Join-Path $packageFullPath 'handoff.md'
$manifestPath = Join-Path $packageFullPath 'manifest.json'
if (-not (Test-Path -LiteralPath $handoffPath -PathType Leaf)) {
    throw "Package is missing handoff.md: $packageFullPath"
}
if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    throw "Package is missing manifest.json: $packageFullPath"
}

$manifestText = [string](Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8)
$handoffText = [string](Get-Content -LiteralPath $handoffPath -Raw -Encoding UTF8)
Assert-NoObviousSecret -Text $manifestText -DisplayName 'manifest.json'
Assert-NoObviousSecret -Text $handoffText -DisplayName 'handoff.md'

try {
    $manifest = $manifestText | ConvertFrom-Json
}
catch {
    throw "manifest.json is not valid JSON: $($_.Exception.Message)"
}

if ([int]$manifest.schema_version -ne 1) {
    throw "Unsupported manifest schema version: $($manifest.schema_version)"
}
if ([string]$manifest.package_kind -ne 'codex-work-context-handoff') {
    throw "Unexpected package kind: $($manifest.package_kind)"
}

$handoffArtifacts = @($manifest.artifacts | Where-Object { [string]$_.path -eq 'handoff.md' })
if ($handoffArtifacts.Count -ne 1) {
    throw 'manifest.json must describe exactly one handoff.md artifact.'
}

$expectedHash = ([string]$handoffArtifacts[0].sha256).ToLowerInvariant()
$actualHash = Get-FileSha256 -Path $handoffPath
if ($actualHash -ne $expectedHash) {
    throw 'handoff.md does not match the SHA-256 hash in manifest.json. The package may be incomplete or modified.'
}

$actualLength = (Get-Item -LiteralPath $handoffPath).Length
if ([long]$handoffArtifacts[0].bytes -ne [long]$actualLength) {
    throw 'handoff.md does not match the byte length in manifest.json.'
}

if (-not [bool]$manifest.safety.human_review_required -or
    [bool]$manifest.safety.raw_codex_session_data_collected -or
    [bool]$manifest.safety.authentication_files_collected -or
    [bool]$manifest.safety.credentials_collected -or
    [bool]$manifest.safety.environment_variables_collected -or
    [bool]$manifest.safety.git_remote_urls_collected) {
    throw 'The package safety declaration is missing or does not meet this importer''s requirements.'
}

$destinationFullPath = Get-AbsolutePath -Path $DestinationPath -BasePath $currentDirectory
$packagePrefix = $packageFullPath + [System.IO.Path]::DirectorySeparatorChar
if ($destinationFullPath.Equals($packageFullPath, [System.StringComparison]::OrdinalIgnoreCase) -or
    $destinationFullPath.StartsWith($packagePrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'DestinationPath cannot be the package directory or a child of it.'
}

if (Test-Path -LiteralPath $destinationFullPath) {
    $destinationItem = Get-Item -LiteralPath $destinationFullPath
    if (-not $destinationItem.PSIsContainer) {
        throw "DestinationPath already exists as a file: $destinationFullPath"
    }

    if (-not $Force) {
        throw "DestinationPath already exists. Choose a new directory or pass -Force to replace only known package files: $destinationFullPath"
    }

    $unexpectedDestinationItems = @(Get-ChildItem -LiteralPath $destinationFullPath -Force | Where-Object { $_.Name -notin $knownArtifactNames })
    if ($unexpectedDestinationItems.Count -gt 0) {
        throw "DestinationPath contains files other than handoff.md and manifest.json. Refusing to overwrite it: $destinationFullPath"
    }
}

if ($PSCmdlet.ShouldProcess($destinationFullPath, 'Import verified portable Codex work-context package')) {
    [void][System.IO.Directory]::CreateDirectory($destinationFullPath)
    [System.IO.File]::WriteAllBytes((Join-Path $destinationFullPath 'handoff.md'), [System.IO.File]::ReadAllBytes($handoffPath))
    [System.IO.File]::WriteAllBytes((Join-Path $destinationFullPath 'manifest.json'), [System.IO.File]::ReadAllBytes($manifestPath))

    [pscustomobject]@{
        ImportedPath = $destinationFullPath
        HandoffPath = (Join-Path $destinationFullPath 'handoff.md')
        ManifestPath = (Join-Path $destinationFullPath 'manifest.json')
        Sha256Verified = $true
        HumanReviewRequired = $true
    }
}
