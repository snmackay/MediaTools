#Set up folders and log file
$CorruptFolder = ".\_Corrupt_Files"
$LogFile = ".\verification_log.txt"
New-Item -ItemType Directory -Force -Path $CorruptFolder | Out-Null
Clear-Content -Path $LogFile -ErrorAction SilentlyContinue

#Find and scan all Opus files
Get-ChildItem -Recurse -Filter *.opus | ForEach-Object {
    $FilePath = $_.FullName
    Write-Host "Checking: $($_.Name)" -ForegroundColor Cyan
    
    #Test decode using FFmpeg and capture error stream
    $Errors = & ffmpeg -v error -i $FilePath -f null - 2>&1
    
    #If errors exist, log them and move the file
    if ($Errors) {
        $ErrorMsg = "[$($_.Name)] CORRUPT: $Errors"
        Add-Content -Path $LogFile -Value $ErrorMsg
        Write-Host "-> CORRUPT! Moving to $CorruptFolder" -ForegroundColor Red
        Move-Item -Path $FilePath -Destination $CorruptFolder -Force
    }
}
Write-Host "Scan complete. Check verification_log.txt for results." -ForegroundColor Green
