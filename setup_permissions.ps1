# Script de PowerShell para configurar permisos en carpetas de descarga
Write-Host "`nConfiguring download folder permissions...`n" -ForegroundColor Cyan

$folders = @(
    "downloads",
    "downloads\audio",
    "downloads\video"
)

foreach ($folder in $folders) {
    # Create folder if it doesn't exist
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
        Write-Host "Folder created: $folder" -ForegroundColor Green
    }
    
    # Configure permissions using icacls
    icacls $folder /grant:r "*S-1-1-0:(OI)(CI)F" /T /C /Q 2>&1 | Out-Null
    
    Write-Host "Permissions configured: $folder" -ForegroundColor Green
}

Write-Host "`nConfiguration complete!`n" -ForegroundColor Yellow
