import psutil

def get_cpu_info():
    cpu_info = {
        'Cores': psutil.cpu_count(logical=False),
        'Threads': psutil.cpu_count(logical=True),
        'Max Frequency': f"{psutil.cpu_freq().max} MHz",
        'Current Frequency': f"{psutil.cpu_freq().current} MHz",
        'Usage': f"{psutil.cpu_percent()}%"
    }
    return cpu_info
