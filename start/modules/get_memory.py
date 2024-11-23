import psutil

def get_memory_info():
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    return {
        "Total RAM": f"{memory.total / (1024**3):.2f} GB",
        "Available RAM": f"{memory.available / (1024**3):.2f} GB",
        "Used RAM": f"{memory.used / (1024**3):.2f} GB",
        "Total Swap": f"{swap.total / (1024**3):.2f} GB",
        "Used Swap": f"{swap.used / (1024**3):.2f} GB",
        "Free Swap": f"{swap.free / (1024**3):.2f} GB"
    }
