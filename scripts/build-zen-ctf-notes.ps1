param(
    [string]$SourceRoot = (Join-Path $PSScriptRoot '..\my_writeups\ZEN_CTFNotesh4g'),
    [string]$OutputRoot = (Join-Path $PSScriptRoot '..\zen-ctf-notes')
)

$ErrorActionPreference = 'Stop'
$source = (Resolve-Path -LiteralPath $SourceRoot).Path
New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null

function Repair-NotionText([string]$Text) {
    if ($Text -match '[Ãâ]') {
        $bytes = [System.Text.Encoding]::GetEncoding(1252).GetBytes($Text)
        return [System.Text.Encoding]::UTF8.GetString($bytes)
    }
    return $Text
}

function Clean-NotionName([string]$Name) {
    return (($Name -replace '\s+[0-9a-f]{32}$', '') -replace '_', ' ').Trim()
}

$notes = foreach ($file in Get-ChildItem -LiteralPath $source -Recurse -File -Filter '*.md') {
    $relative = $file.FullName.Substring($source.Length + 1).Replace('\', '/')
    $relativeParts = $relative.Split('/')
    $folders = if ($relativeParts.Length -gt 1) { @($relativeParts[0..($relativeParts.Length - 2)] | ForEach-Object { Clean-NotionName $_ }) } else { @() }
    # Every nested export page starts beneath the Notion collection folder.
    if ($folders.Count -gt 0) { $folders = @($folders | Select-Object -Skip 1) }
    $title = Clean-NotionName ([System.IO.Path]::GetFileNameWithoutExtension($file.Name))
    $group = if ($folders.Count) { $folders -join ' / ' } elseif ($title -eq 'CTF Checklists + Tools + Syntax') { 'Start Here' } else { 'CTF Checklists' }
    $text = Repair-NotionText (Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8)
    if (-not [string]::IsNullOrWhiteSpace($text)) {
        [ordered]@{
            id = ($relative -replace '\s+[0-9a-f]{32}(?=\.md$)', '' -replace '[^A-Za-z0-9]+', '-').Trim('-').ToLowerInvariant()
            title = $title
            group = $group
            source = $relative
            format = 'MD'
            text = $text.Trim()
        }
    }
}

$json = @($notes) | ConvertTo-Json -Depth 5 -Compress
[System.IO.File]::WriteAllText((Join-Path $OutputRoot 'notes-data.js'), "window.ZEN_NOTES=$json;", [System.Text.UTF8Encoding]::new($false))
Write-Host "Built $($notes.Count) Markdown notes from $source"
