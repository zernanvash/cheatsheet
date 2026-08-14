param(
    [string]$SourceRoot = (Join-Path $PSScriptRoot '..\_source_zen'),
    [string]$OutputRoot = (Join-Path $PSScriptRoot '..\zen-ctf-notes')
)

$ErrorActionPreference = 'Stop'
$source = (Resolve-Path -LiteralPath $SourceRoot).Path
New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $OutputRoot 'assets') | Out-Null
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Get-DocxText([string]$Path) {
    $archive = [System.IO.Compression.ZipFile]::OpenRead($Path)
    try {
        $entry = $archive.GetEntry('word/document.xml')
        if (-not $entry) { return '' }
        $reader = [System.IO.StreamReader]::new($entry.Open())
        try { [xml]$xml = $reader.ReadToEnd() } finally { $reader.Dispose() }
        $manager = [System.Xml.XmlNamespaceManager]::new($xml.NameTable)
        $manager.AddNamespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')
        $paragraphs = foreach ($paragraph in $xml.SelectNodes('//w:body/w:p | //w:body/w:tbl//w:p', $manager)) {
            $pieces = foreach ($node in $paragraph.SelectNodes('.//w:t | .//w:tab | .//w:br', $manager)) {
                if ($node.LocalName -eq 'tab') { "`t" } elseif ($node.LocalName -eq 'br') { "`n" } else { $node.InnerText }
            }
            ($pieces -join '').TrimEnd()
        }
        return (($paragraphs -join "`n") -replace "`n{3,}", "`n`n").Trim()
    } finally { $archive.Dispose() }
}

$notes = foreach ($file in Get-ChildItem -LiteralPath $source -Recurse -File | Where-Object Extension -in '.txt', '.docx') {
    $relative = $file.FullName.Substring($source.Length + 1).Replace('\', '/')
    $parts = $relative.Split('/')
    $group = if ($parts.Length -gt 1) { ($parts[0..($parts.Length - 2)] -join ' / ') } else { 'CTF Quick Reference' }
    $title = [System.IO.Path]::GetFileNameWithoutExtension($file.Name) -replace '_', ' '
    $text = if ($file.Extension -eq '.docx') { Get-DocxText $file.FullName } else { Get-Content -LiteralPath $file.FullName -Raw }
    if (-not [string]::IsNullOrWhiteSpace($text)) {
        [ordered]@{ id = ($relative -replace '[^A-Za-z0-9]+', '-').Trim('-').ToLowerInvariant(); title = $title; group = $group; source = $relative; format = $file.Extension.TrimStart('.').ToUpperInvariant(); text = $text.Trim() }
    } else {
        Write-Warning "Skipped empty source: $relative"
    }
}

$images = foreach ($file in Get-ChildItem -LiteralPath $source -File -Filter '*.png') {
    Copy-Item -LiteralPath $file.FullName -Destination (Join-Path $OutputRoot ('assets\' + $file.Name)) -Force
    [ordered]@{ id = ([System.IO.Path]::GetFileNameWithoutExtension($file.Name) -replace '[^A-Za-z0-9]+', '-').Trim('-').ToLowerInvariant(); title = [System.IO.Path]::GetFileNameWithoutExtension($file.Name); group = 'Visual References'; source = $file.Name; format = 'PNG'; image = ('assets/' + $file.Name) }
}

$all = @($notes) + @($images)
$json = $all | ConvertTo-Json -Depth 5 -Compress
[System.IO.File]::WriteAllText((Join-Path $OutputRoot 'notes-data.js'), "window.ZEN_NOTES=$json;", [System.Text.UTF8Encoding]::new($false))
Write-Host "Built $($notes.Count) notes and $($images.Count) images in $OutputRoot"
