from datetime import datetime

def get_local_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
