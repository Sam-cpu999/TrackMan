import os

def get_drives():
    drive_info = []
    drives = os.popen("wmic logicaldisk get name").read().strip().split()
    for drive in drives[1:]: 
        total_space = os.popen(f"wmic logicaldisk where name='{drive}' get size").read().strip().split()[1]
        free_space = os.popen(f"wmic logicaldisk where name='{drive}' get freespace").read().strip().split()[1]
        drive_info.append(f"Drive {drive}: Total: {total_space} bytes, Free: {free_space} bytes")
    return "\n".join(drive_info)
